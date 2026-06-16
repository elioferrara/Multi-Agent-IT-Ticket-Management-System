# Carico le chiavi per i modelli
from dotenv import load_dotenv
load_dotenv()
# Librerie Agno
from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.groq import Groq
# Librerie personali
from database.database import db

# region technical_human.

technical_human = Agent(
    name="technical-human",
    model=Groq(id="llama-3.1-8b-instant"),
    db=db,
    instructions = ["Il tuo compito è simulare la chiamata ad un agente umano."
                    "Ad ogni domanda devi rispondere con la seguente frase:"
                    "'Presto un tecnico verrà ad aiutarti, rimani in attesa'"
                    "Rispondi in italiano"
    ],
)
# endregion