# Carico le chiavi per i modelli
from dotenv import load_dotenv
load_dotenv()
# Librerie Agno
from agno.agent import Agent
from agno.tools import tool
from agno.models.groq import Groq

# Librerie personali
from database.database import db
from knowledge.knowledge import compliance_knowledge
from optimization.optimization import compression
from agents.technical_agent import technical_agent
from agents.technical_human import technical_human
from agents.security_agent import security_gatekeeper


# region Delegate tools.
# Definisco un tool per delegare all'agente tecnico
@tool # Decoratore che autogenera la definizione della signature del metodo, quella che finisce all'LLM
def delegate_to_technical_agent(user_message: str):
    # Documentazione per permettere la costruzione del file JSON da dare in pasto all'LLM
    """ Delega la richiesta all'agente tecnico. Passa esattamente il messaggio completo ricevuto dall'utente, senza riassumerlo.

    Args:
        user_message: il messaggio dell'utente

    Returns:
        La risposta dell'agente responsabile
    """

    answer = technical_agent.run(user_message)

    return answer.content

# DEBUG

# Definisco un tool per delegare al tecnico umano
@tool # Decoratore che autogenera la definizione della signature del metodo, quella che finisce all'LLM
def delegate_to_human_agent(task: str, agent: Agent = None):
    # Documentazione per permettere la costruzione del file JSON da dare in pasto all'LLM
    """ Delega la richiesta all'tecnico umano

    Args:
        task: il problema che dev'essere risolto

    Returns:
        La risposta dell'agente responsabile
    """

    answer = technical_human.run(task)

    return answer.content
#endregion
# region technical_team_leader.
# Definisco un gruppo di problemi che voglio delegare all'agente tecnico
WHITELIST = [
    "problemi di accesso o login",
    "configurazione o errori della VPN",
    "reset password",
    "problemi con la stampante",
    "richieste di informazioni tecniche generali"
]

# Definisco un agente leader tecnico
technical_team_leader = Agent(
    name="technical_team_leader",
    model=Groq(id="openai/gpt-oss-20b", temperature=0.0),
    db=db,
    instructions=["Sei il leader italiano di un team che risolve ticket informatici. Il tuo compito è orchestrare le richieste. \n"
                  "REGOLE DI SMISTAMENTO: \n"
                  "1. Usa il tool 'delegate_to_technical_agent' nei seguenti casi:\n"
                 f"   - La richiesta originale riguarda un tema in questa lista: {WHITELIST}.\n"
                  "   - OPPURE l'utente sta fornendo dati, codici o risposte a una domanda posta in precedenza dall'agente tecnico.\n"
                  "2. In tutti gli altri casi di assistenza tecnica, usa il tool 'delegate_to_human_agent'.\n\n"
                  " REGOLE DI CONVERSAZIONE: \n"
                  "Se l'interazione è conversazionale o la richiesta non è ben formulata, rispondi cercando di chiarire al meglio il problema da risolvere."
                  "Se la richiesta non ha a che fare con procedure informatiche, rispondi dicendo che non puoi aiutare."
                  "REGOLE DI OUTPUT: \n"
                  "DIVIETO TASSATIVO DI RIFORMULAZIONE: Una volta che il tool (technical_agent o human_agent) ha risposto, "
                  "il tuo compito è TERMINATO. È ASSOLUTAMENTE VIETATO aggiungere introduzioni (es. 'Certamente!', 'Ecco la risposta'), "
                  "è vietato aggiungere saluti, commenti o scuse. "
                  "Devi prendere l'esatto testo restituito dal sotto-agente e fare un COPIA-INCOLLA LETTERALE. "
                  "Se aggiungi una sola parola di testa tua, l'intera procedura fallirà."],
    tools=[delegate_to_technical_agent, delegate_to_human_agent],
    tool_call_limit=1,
    # Aggiungo un pre hook per i controlli di sicurezza (Evitare injection, jailbreak, ecc..)
    pre_hooks=[security_gatekeeper],
    add_history_to_context=True,
    num_history_messages=4,
    )
# endregion