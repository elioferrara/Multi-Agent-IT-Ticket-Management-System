# Carico le chiavi per i modelli
from dotenv import load_dotenv
load_dotenv()
# LIBRERIE AGNO
from agno.agent import Agent
from agno.models.groq import Groq
# Librerie per i guardrails (pre hook e post hook)
from agno.exceptions import CheckTrigger, InputCheckError, OutputCheckError
from agno.run.agent import RunInput, RunOutput
from agno.guardrails import PromptInjectionGuardrail
# LIBRERIE GENERALI
import re # Utile per catturare il testo tra due tag
# LIBRERIE PERSONALI
from database.database import db
from knowledge.knowledge import compliance_knowledge
from optimization.optimization import compression


# region compliance_agent.
compliance_agent = Agent(
    name="compliance_agent",
    model=Groq(id="openai/gpt-oss-120b", temperature=0.0),
    db=db,
    instructions=[
        "Sei un esperto valutatore di conformità aziendale. Ricevi in input le risposte del nostro agente tecnico: Il tuo compito è valutare le sue risposte.",
        "Per conoscere le regole aziendali, devi utilizzare OBBLIGATORIAMENTE il tool 'search_knowledge'. Quello che trovi tramite il tool è il 'Manuale delle Policy'. Non usare la tua memoria o il tuo addestramento.",
        "Segui rigidamente questa procedura di valutazione: ",
        "1. Usa il tool 'search_knowledge' per recuperare le linee guida da rispettare.",
        "2. Verifica se il messaggio è conforme alle linee guida.",
        "3. Prendi una decisione insindacabile: se rispetta tutte le linee guida, APPROVED, altrimenti BLOCKED.",
        "4. Scrivi l'output seguendo rigidamente questa struttura:"
        "  <status>APPROVED oppure BLOCKED</status>\n"
        "  <reason>Spiega qui dettagliatamente i motivi della tua decisione, citando le linee guida del 'manuale delle policy' (Utile per il debugging)</reason>\n"
        "  <corrected_text>Inserisci qui la frase riformulata SOLO SE lo stato è BLOCKED.</corrected_text>, se lo stato è APPROVED, non aggiungere altro.\n"
    ],
    stream=False,
    knowledge=compliance_knowledge,
    search_knowledge=True,
    # Ottimizzazione
    compression_manager=compression,
)

# Definisco una classe per istanziare oggetti che possono essere usati come post_hook.
class ComplianceGatekeeper:
    def __init__(self, agent):
        self.agent=agent
        self.__name__="ComplianceGatekeeper"
        # Definiamo un metodo call per usare l'agente come post_hook, in base alle linee guida di Agno (vedi documentazione)
    def __call__(self, run_output: RunOutput):
        # Prende il messaggio del tecnico
        technical_answer=run_output.content
        # Lancia il ragionamento dell'agente
        response=self.agent.run(technical_answer)
        # Formattiamo la decisione
        decision = response.content.strip().upper()

        # DEBUG
        print("\n================================================")
        print(f"DEBUG GATEKEEPER - Input Tecnico: {technical_answer}")
        print(f"DEBUG GATEKEEPER - Risposta Modello: '{decision}'")
        print("================================================\n")

        if decision.startswith("<STATUS>BLOCKED"):
            # Stampa il messaggio riformulato
            match = re.search(r"<corrected_text>(.*?)</corrected_text>", response.content, re.DOTALL)
            run_output.content = match.group(1)
            return run_output
        

compliance_gatekeeper = ComplianceGatekeeper(compliance_agent)