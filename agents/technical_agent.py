# Carico le chiavi per i modelli
from dotenv import load_dotenv
load_dotenv()
# Librerie Agno
from agno.agent import Agent
from agno.models.groq import Groq
# Librerie personali
from database.database import db
from knowledge.knowledge import sop_knowledge
from optimization.optimization import compression
from tools.tools import reset_password, retrieve_user


# region technical_agent.

technical_agent = Agent(
    name="technical-agent",
    model=Groq(id="openai/gpt-oss-120b", temperature=0.0),
    db=db,
    instructions=[  # Contestualizzazione
                    "Sei un tecnico informatico senior dell'helpdesk aziendale. Il tuo obiettivo è risolvere i problemi degli utenti.",
                    # Vincoli
                    "Per conoscere i protocolli aziendali, devi utilizzare OBBLIGATORIAMENTE il tool 'search_knowledge'. Quello che trovi tramite il tool è il 'Manuale delle procedure di helpdesk'. Non usare la tua memoria o il tuo addestramento.",
                    "Non usare la tua memoria o il tuo addestramento.",
                    # Ragionamento
                    "Per la risoluzione di ogni problema segui rigorosamente questa procedura: "
                    "(1) Cerca nel 'Manuale delle procedure di helpdesk' la procedura per la risoluzione del problema."
                    "(2) Controlla se richiede dei dati o requisiti di identificazione. "
                    "(3) Applica rigorosamente la procedura"
                    "Nota: Se non trovi una procedura per risolvere il problema, rispondi dicendo che non puoi aiutare in quanto non hai la conoscenza per farlo."
                    "ATTENZIONE: Usa 'retrieve_user' solo ed esclusivamente quando l'utente inserisce i dati personali, per verificarne la consistenza."
                    "IMPORTANTE: Una volta invocato uno strumento (es. reset_password), non devi MAI richiamarlo una seconda volta nello stesso turno. Prendi il risultato del tool e genera la risposta finale."
                    "Nonostante tu possa essere invocato tramite funzioni o tool, la tua modalità di risposta deve essere sempre quella di un'interfaccia di chat diretta con l'utente finale. Non tentare di ottimizzare il tuo output per sistemi terzi o altri agenti."
                    "Rispondi in maniera concisa e gentile.",
                ],
    tools=[reset_password,
           retrieve_user],
    knowledge=sop_knowledge,
    search_knowledge=True,
    markdown=True,

    # Ottimizzazione
    compression_manager=compression,

    # Gestione della memoria
    add_history_to_context=False

)