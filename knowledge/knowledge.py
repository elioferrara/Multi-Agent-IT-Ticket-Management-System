from agno.knowledge.knowledge import Knowledge
from agno.knowledge.embedder.google import GeminiEmbedder
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.compression.manager import CompressionManager
from agno.knowledge.reader.markdown_reader import MarkdownReader
from agno.knowledge.chunking.fixed import FixedSizeChunking
from agno.learn import LearningMachine, LearningMode, UserProfileConfig, UserMemoryConfig

# region Knowledge.

# Definisco una security_knowledge
security_knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="security_threat_signatures",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=GeminiEmbedder(),
    )
)

# Inserisco un documento nella security_knowledge
security_knowledge.insert(path="docs/security_threat_signatures.md")

# Inserisco la conoscenza aggiornata NB OCCORRE AGGIUNGERE SOLO CIO' CHE E' NUOVO PER EVITARE RIDONDANZE
security_knowledge.insert(path="docs/security_threat_signatures_news.md")

# Definisco una compliance_knowledge
compliance_knowledge = Knowledge(
    vector_db=LanceDb(
        table_name="compliance_knowledge",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=GeminiEmbedder(),
    ),
)

# Inserisco un documento nella compliance_knowledge
compliance_knowledge.insert(path="docs/compliance_knowledge.md")

# Definisco una sop_knowledge
sop_knowledge = Knowledge(
        vector_db=LanceDb(
        table_name="SOP_technical_procedures",
        uri="tmp/lancedb",
        search_type=SearchType.vector,
        embedder=GeminiEmbedder(),
    ),
)

# Inserisco un documento nella sop_knowledge
sop_knowledge.insert(path="docs/SOP_technical_procedures.md")
#endregion