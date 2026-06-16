from agno.compression.manager import CompressionManager
from agno.models.groq import Groq

#region CompressionManager.

compression = CompressionManager(
    model=Groq(id="llama-3.3-70b-versatile"),
    compress_tool_results=True,
    compress_token_limit=1000,
)
#endregion