#     Multi-Agent-IT-Ticket-Management-System



Sistema multi agente per la gestione di ticket informatici basato su [Agno](https://docs.agno.com/), Google Gemini e Groq.
Questo progetto implementa un sistema multi-agente intelligente e modulare, progettato per automatizzare la gestione dei ticket di supporto IT. Sfruttando il framework Agno, il sistema organizza i flussi di lavoro tramite agenti specializzati — ognuno dotato di conoscenze, istruzioni e strumenti dedicati — che collaborano per risolvere le richieste in modo efficiente e accurato.
## Prerequisiti

- **Python 3.12+** (vedi [.python-version](.python-version))
- **[uv](https://docs.astral.sh/uv/)** come package manager
- Una **API key di Google Gemini**
- Una **API key di Groq**


## 1. Scaffolding iniziale (solo al primo setup di un progetto da zero)

Se stai creando il progetto da zero, in una cartella vuota lancia:

```powershell
uv init .
```

Questo crea `pyproject.toml`, `.python-version` e gli altri file base.

`uv init` genera anche un `main.py` di esempio: puoi cancellarlo, non viene usato dal progetto (il punto di ingresso è [gestione_ticket.py](gestione_ticket.py)).

## 3. Creare il virtual environment e installare le dipendenze

Crea il venv:

```powershell
uv venv
```

Sincronizza le dipendenze dichiarate in [pyproject.toml](pyproject.toml) / [uv.lock](uv.lock):

```powershell
uv sync
```

Attiva il venv (PowerShell su Windows):

```powershell
.venv\Scripts\Activate.ps1
```

Su bash/zsh:

```bash
source .venv/bin/activate
```

## 4. Creare il file `.env`

Nella root del progetto crea un file `.env` con la chiave ottenuta al passo 1:

```dotenv
GOOGLE_API_KEY=la-tua-chiave-qui
GROQ_API_KEY=la-tua-chiave-qui
```

Il file `.env` è già in [.gitignore](.gitignore): non verrà committato.
[gestione_ticket.py](gestione_ticket.py) lo carica automaticamente con `python-dotenv` prima di importare Agno.

## 5. Avviare il bot

Con il venv attivo:

```powershell
fastapi dev recipebot.py
```

Il server di sviluppo si avvia su `http://127.0.0.1:8000`. Endpoint utili:

- `http://127.0.0.1:8000/docs` — Swagger UI di FastAPI
- `http://127.0.0.1:8000` — root dell'AgentOS

Al primo avvio l'agente:

- crea il database SQLite in `tmp/technical_agent.db`
- crea l'indice vettoriale LanceDB in `tmp/lancedb`
- ingerisce i file di knowledge da [docs/](docs/)

## Escludere `tmp/` da git

La cartella `tmp/` contiene stato runtime che non va versionato. Aggiungi al [.gitignore](.gitignore):

```gitignore
tmp/**
```

In questo repo l'esclusione è già presente. Se hai già committato per errore qualche file dentro `tmp/`, rimuovilo dall'indice mantenendolo su disco con:

```powershell
git rm -r --cached tmp
```

## Struttura del progetto

```
Agent_GestioneTicket/
├── agents/             # Definizione e logica degli agenti
├── database/           # Gestione dati e persistenza
├── docs/               # Knowledge base (security_knowledge, sop_knowledge, compliance_knowledge)
├── knowledge/          # Inizializzazione della knowledge base (RAG)
├── optimization/       # Logiche di ottimizzazione del sistema
├── tools/              # Strumenti personalizzati (tool) per gli agenti
├── gestione_ticket.py  # Punto di ingresso principale (main)
├── pyproject.toml      # Definizione dipendenze (uv)
├── uv.lock             # Lockfile per versioni dipendenze
└── .env                # Variabili d'ambiente (NON committare!)```

## Troubleshooting

- **`GOOGLE_API_KEY` non trovata**: verifica che `.env` esista nella stessa cartella da cui lanci `fastapi dev` e che la variabile sia scritta senza spazi attorno a `=`.
- **`fastapi: command not found`**: il venv non è attivo, oppure `uv sync` non è stato eseguito.
- **Errori da LanceDB/Tantivy al primo avvio**: cancella la cartella `tmp/` e riavvia per rigenerare gli indici.

