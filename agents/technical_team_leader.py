# Carico le chiavi per i modelli
from dotenv import load_dotenv
load_dotenv()
# Librerie Agno
from agno.agent import Agent
from agno.team.team import Team
from agno.tools import tool
from agno.models.groq import Groq

# Librerie personali
from database.database import db
from knowledge.knowledge import compliance_knowledge
from optimization.optimization import compression
from agents.technical_agent import technical_agent
from agents.technical_human import technical_human
from agents.security_agent import security_gatekeeper
from agents.compliance_agent import compliance_gatekeeper

# region Team

# Definisco un gruppo di problemi che voglio delegare all'agente tecnico
WHITELIST = [
    "problemi di accesso o login",
    "configurazione o errori della VPN",
    "reset password",
    "problemi stampante",
    "Invio dati personali"
]

# Definisco un agente leader tecnico
technical_team_leader = Team(name="technical_team_leader",
                               model=Groq(id="openai/gpt-oss-20b", temperature=0.1),
                               db=db,
                               instructions="Sei il leader di un team che risolve ticket informatici. Il tuo compito è orchestrare le richieste."
                  "REGOLE DI ORCHESTRAZIONE: "
                  "Usa il tool 'delegate_to_technical-agent' solo ed esclusivamente in questi due casi: "
                  "(1) L'utente invia dei suoi dati personali(es. 'ID-XXXX' ) 'ID-XXXX'. In questo caso inoltra la richiesta al technical-agent senza richiedere ulteriori informazioni."
                  f"(2) Il problema da gestire riguarda un tema in questa lista: \n- {WHITELIST} \n"
                  "Usa il tool 'delegate_to_human-agent' in questi casi: " \
                  "1. Il problema da risolvere non è nella whitelist."
                  "2. Se l'utente riferisce che una procedura suggerita dal 'technical-agent' non ha prodotto risultati,"
                  "In questo caso non fare ulteriori domande e delega immediatamente al tecnico umano."
                  "Casi tipo: 'non ha funzionato', 'il problema persiste', 'ho provato ma nulla', 'ancora non va'"
                  "GESTIONE DELLA CONVERSAZIONE: "
                  "Se l'interazione è conversazionale o la richiesta non è ben formulata, rispondi cercando di chiarire al meglio il problema da risolvere."
                  "Se ricevi un messaggio di apertura di conversazione, rispondi in maniera cordiale richiedendo informazioni sul problema da risolvere."
                  "Se ricevi un messaggio di chiusura di conversazione risolutiva, del tipo 'Ho risolto', rispondi cordialmente in maniera simile a 'Siamo lieti di averti aiutato a risolvere il problema.'"
                  "Se la richiesta non ha a che fare con richieste di assistenza informatiche lavorative, rispondi dicendo che non puoi aiutare."
                  "RICORDA: Se l'utente invia i suoi dati personali, devi delegare il compito al technical agent, sarà lui a gestirli",
                  members=[technical_human, technical_agent],
                  
                  determine_input_for_members=False,
                  respond_directly=True,

                  add_team_history_to_members=True,

                  # guardrails
                  pre_hooks=[security_gatekeeper],
                  post_hooks=[compliance_gatekeeper]
)

# endregion