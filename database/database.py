from agno.db.sqlite import SqliteDb

# Database per salvare le sessioni, lo possiamo usare per più agenti
db=SqliteDb(db_file="tmp/technical_agent.db")

# Definisco un dizionario con key=ID dell 'utente e values una serie di attributi
# ! Ipotetico DB contenente i dati degli utenti di un'azienda ! 

users = {
    "ID-20054087": {
        "nome": "Elio Ferrara",
        "password": "GFRES2102!",
        "ufficio": "AI",
        "stato": "Active",
    },
    "ID-31165098": {
        "nome": "Elena Bianchi",
        "password": "TRTWS2203?",
        "ufficio": "Amministrazione",
        "stato": "Locked",
    },
    "ID-45576109": {
        "nome": "Luca Verdi",
        "password": "KLPZA2304#",
        "ufficio": "Sviluppo",
        "stato": "Active",
    },
    "ID-58897210": {
        "nome": "Giulia Neri",
        "password": "XCVBN2405*",
        "ufficio": "Risorse Umane",
        "stato": "Disabled",
    },
    "ID-62218321": {
        "nome": "Alessandro Riva",
        "password": "QWERT2506$",
        "ufficio": "Sviluppo",
        "stato": "Active",
    },
}

#endregion