import os

from dotenv import load_dotenv
load_dotenv()

from agno.models.groq import Groq
from agno.models.mistral import MistralChat
from agno.models.google import Gemini

from agno.agent import Agent
from agno.os import AgentOS
from agno.db.sqlite import SqliteDb

# Librerie per impostare un workflow
from agno.workflow.workflow import Workflow
from agno.workflow.step import Step, StepInput, StepOutput   
"""
from agno.tools.website import WebsiteTools
from agno.tools.firecrawl import FirecrawlTools
from agno.tools.serper import SerperTools
from agno.tools.websearch import WebSearchTools
from agno.tools.hackernews import HackerNewsTools
from agno.tools.duckduckgo import DuckDuckGoTools """
from agno.tools.tavily import TavilyTools

groq = Groq(id="openai/gpt-oss-120b")
mistral = MistralChat(id="mistral-large-latest")
gemini = Gemini(id="gemini-2.5-flash-lite")

# Seleziono una lista di siti affidabili da cui ricavare informazioni su vulnerabilità
reliable_sites="https://atlas.mitre.org/"

db= SqliteDb(db_file="tmp/editor_agent.db")

research_agent = Agent(
    name='editor_agent',
    model=groq,
    instructions=[
    "Sei un Detection Engineer ed esperto di Cyber Security specializzato nella difesa di LLM e sistemi multi-agente.",
    "Il tuo unico compito è cercare su internet nuove tecniche di attacco, varianti di jailbreak, prompt injection o exploit emergenti rivolti agli LLM.",

    "CRITERIO DI SELEZIONE RIGIDO:",
    "- NON raccogliere notizie generiche su vulnerabilità infrastrutturali.",
    "- Cerca solo attacchi che avvengono via CHAT o tramite manipolazione degli input testuali/multimodali dell'LLM.",
    
    "FORMATO DI OUTPUT OBBLIGATORIO:",
    "Devi estrarre le informazioni e organizzarle in un file Markdown strutturato ESATTAMENTE come in questo esempio di riferimento:",
    
    "### [Nome della Categoria di Attacco o Nuova CVE]",
    "Descrizione sintetica del funzionamento della minaccia.",
    "#### Firme Semantiche e Frasi Tipiche:",
    "* \"[Inserisci una frase reale o una stringa di attacco tipica usata dagli hacker]\"",
    "* \"[Inserisci una seconda variante di frase o payload tipico]\"",
    
    "REGOLE DI SCRITTURA:",
    "1. Le 'Firme Semantiche' devono contenere le esatte parole chiave, frammenti di codice o strutture di frasi che un Security Agent può intercettare leggendo i log della chat.",
    "2. Scrivi l'intero output in lingua italiana."

    "NON fare più di tre chiamate a TavilyTools."

],
    tools=[TavilyTools(
        max_tokens=2000,
         )]
)

# Definisco che dato un input di testo ne crea un file md e crea un file docs/security_threat_signatures_news.md
def create_markdown_file(step_input: StepInput, session_state=None, folder_path: str="docs/"):
    """Prende l'output dell'agente e lo salva in un file .md"""

    file_name="security_threat_signatures_news.md"

    file_path=os.path.join(folder_path,file_name)

    try:
        with open(file_path, 'w', encoding="utf-8") as f:
                f.write(step_input.previous_step_content)
                print("La scrittura del file è andata a buon fine")
                return True
    except Exception as e:
         print("C'è stato un errore durante la scrittura del file")
         return False


# workflow(research_agent, create_markdown_file)

research_workflow = Workflow(
    name="ResearchWorkflow",
    description="Pipeline a 2 step: ricerca, scrittura",
    db=db,
    steps=[
        Step(name="research_news", agent=research_agent),
        Step(name="create_file", executor=create_markdown_file),
    ],
)


"""
editor_agent.print_response(
    "Cerca le novità dell'ultimo mese (maggio 2026) relativi agli attacchi agli LLMs sui siti di cybersecurity più affidabili",
    markdown=True
)
"""


agent_os = AgentOS(
    name="editor_agent",
    agents=[research_agent],
    workflows=[research_workflow],
    db=db,
    tracing=True,
)

app = agent_os.get_app()