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
from agents.compliance_agent import compliance_gatekeeper


# region technical_agent.

technical_agent = Agent(
    name="technical_agent",
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
                    "ATTENZIONE: Usa 'retrieve_user' solo ed esclusivamente quando l'utente inserisce i dati personali, per verificarne la consistenza."
                    
                    "Rispondi in maniera concisa e gentile.",
                ],
    tools=[# ReasoningTools(add_instructions=True),
           reset_password,
           retrieve_user],
    knowledge=sop_knowledge,
    search_knowledge=True,
    markdown=True,

    # Aggiungo un post hook
    post_hooks=[compliance_gatekeeper],
    # Ottimizzazione
    compression_manager=compression,

    # Soluzione 2. Inietto nel prompt solo i messaggi
    add_history_to_context=True,
    num_history_messages=4

)