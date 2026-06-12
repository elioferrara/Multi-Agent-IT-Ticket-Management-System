# Librerie Agno
from agno.agent import Agent
from agno.tools import tool
# Librerie personali
from database.database import users
# region Login tools.

# Definisco un tool per controllare lo stato dell'utente nel DB
@tool # Decoratore che autogenera la definizione della signature del metodo, quella che finisce all'LLM
# Definisco un tool per recuperare i dati dell'utente
def retrieve_user(username):
    """ Recupera i dati relativi ad un utente dato il suo username
    
    Tool READ-ONLY (rischio basso): non modifica nessuno stato esterno.

    Args:
        username: il codice identificativo univoco del dipendente

    Returns:
        Dizionario dei dati disponibili per l'username in questione.
        Se l'usernamen non c'è nel DB, restituisce un messaggio di errore
    """

    try:
        return users[username]
    except KeyError:
        raise ValueError(f"L'utente '{username}' non esiste nel database.")

# Definisco un tool per il reset della password
@tool # Decoratore che autogenera la definizione della signature del metodo, quella che finisce all'LLM
def reset_password(username):
    # Documentazione per permettere la costruzione del file JSON da dare in pasto all'LLM
    """ Genera una password temporanea per un'utente che vuole cambiarla

    Tool STATE UPDATE (rischio alto): sovrascrive la password esistente

    Args:
        username: il codice identificativo univoco del dipendente, non il suo nome!

    Returns:
        La nuova password temporanea generata
    """
    # Operazioni che deve compiere la funzione
    pssw_generated="ChangeMe123!"
    users[username] = pssw_generated
    print(users)

    return pssw_generated
#endregion


# Definisco una funzione che dato un input di testo ne crea un file md e crea un file docs/security_threat_signatures_news.md
import os

# region Functions.
def create_markdown_file(agent_response_text: str, folder_path: str="docs/"):
    """Prende l'output dell'agente e lo salva in un file .md"""

    file_name="security_threat_signatures_news.md"

    file_path=os.path.join(folder_path,file_name)

    try:
        with open(file_path, 'w', encoding="utf-8") as f:
                f.write(agent_response_text)
                print("La scrittura del file è andata a buon fine")
                return True
    except Exception as e:
         print("C'è stato un errore durante la scrittura del file")

         return False
# Debug  
# testo= "Ciao, come stai?"
# create_markdown_file(testo)

#endregion