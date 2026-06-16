from agno.agent import Agent
from agno.models.groq import Groq
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.db.sqlite import SqliteDb

from agno.knowledge import Knowledge
from agno.learn import LearningMachine, LearningMode, LearnedKnowledgeConfig

from database.database import db

learnings_knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="technical_human_knowledge",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=GeminiEmbedder(),
    ),
)


groq = Groq(id="openai/gpt-oss-20b")

retain_agent = Agent(
    name="retain_agent",
    model=groq,
    db=db,
    instructions=["Sei un agente di retain per un sistema di gestione ticket. Il tuo compito è decidere cosa mantenere in memoria.",
                  "Fai una query di ricerca per turno, non di più.",
                  "In particolare devi riorganizzare le informazioni che ti vengono date da un tecnico in questo modo: ",
                  "(1) Problema: descrizione del problema da risolvere.",
                  "(2) Soluzione: descrizione della soluzione applicata.",
                  "Rispondi in italiano."
                ],
    learning=LearningMachine(
        knowledge=learnings_knowledge,
        learned_knowledge=LearnedKnowledgeConfig(mode=LearningMode.PROPOSE),
    ),
    add_history_to_context=True,
    num_history_messages=2,
)