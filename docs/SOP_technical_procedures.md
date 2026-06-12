# 📘 MANUALE OPERATIVO IT - TECHCORP SOLUTIONS
**Documento di Riferimento Interno per Supporto Tecnico L1/L2**
**Stato:** Operativo | **Ultimo Aggiornamento:** Maggio 2026

---

## SOP-001: Gestione Credenziali e Accessi (Identity Management)
**Obiettivo:** Risoluzione di problemi legati all'accesso agli account aziendali e gestione delle identità in Active Directory.

### 1.1 Procedura di Identificazione Utente (VINCOLO DI SISTEMA BLOCCANTE)
Prima di eseguire qualsiasi diagnosi o operazione, l'operatore DEVE obbligatoriamente raccogliere la seguente checklist completa. È severamente vietato procedere senza:

[ ] 1. **Codice Dipendente** (deve rispettare il formato `ID-XXXXX`)
[ ] 2. **Ufficio di Appartenenza**

**🔴 LOGICA DI VALIDAZIONE (IF/THEN):**
- **SE** l'utente fornisce SOLO un dato (es. solo l'ufficio) -> FERMATI. Non applicare nessuna SOP. Rispondi chiedendo specificamente il dato mancante.
- **SE** l'utente non fornisce NESSUN dato -> FERMATI. Chiedi entrambi i dati.
- **SE** l'utente ha fornito ENTRAMBI i dati -> Procedi all'analisi del problema.
- **SE** l'utente rifiuta o i dati non esistono -> Termina la procedura e indirizza ad HR.

### 1.2 Reset Password e Sblocco Account
* **Analisi dello Stato:** Verificare tramite console se l'account risulta `Locked` (Bloccato per tentativi errati) o `Disabled` (Disabilitato).
* **Azione per Account Bloccato:** Eseguire esclusivamente lo sblocco (`Unlock`) senza modificare la password attuale.
* **Azione per Reset Password:** Generare una password temporanea che rispetti i seguenti criteri:
    - Minimo **14 caratteri**.
    - Presenza di almeno una **Maiuscola**, un **Numero** e un **Simbolo Speciale** (`!`, `@`, `#`, `$`).
* **Post-Operazione:** Comunicare all'utente che la password ha una validità di **24 ore** e che il sistema richiederà il cambio obbligatorio al primo accesso.

---

## SOP-002: Troubleshooting Connessione VPN (GlobalConnect)
**Obiettivo:** Supporto per dipendenti in smart working che riscontrano difficoltà di accesso alla rete interna.

### 2.1 Tabella Codici Errore VPN
L'operatore deve consultare la seguente tabella per fornire la soluzione immediata:

| Codice Errore | Significato | Azione Correttiva |
| :--- | :--- | :--- |
| **ERR-VPN-401** | Credenziali Invalide | Verificare se la password è scaduta o l'account è bloccato (vedi SOP-001). |
| **ERR-VPN-505** | Certificato Scaduto | Inviare il link per il download del nuovo certificato: `https://tools.techcorp.local/vpn-cert`. |
| **ERR-VPN-900** | MFA non sincronizzato | Chiedere all'utente di riavviare l'app *Authenticator* sul cellulare aziendale. |
| **ERR-VPN-000** | No Internet | Verificare che l'utente non sia in modalità aereo o connesso a una rete Wi-Fi pubblica instabile. |

### 2.2 Requisiti di Performance
- La VPN **non supporta** connessioni via Hotspot Mobile per applicazioni pesanti (es. CAD o SAP).
- Se il valore di **Latency (Ping)** verso il server aziendale supera i **150ms**, la sessione verrà chiusa automaticamente dal firewall.

---

## SOP-003: Gestione Stampanti di Rete e Periferiche
**Obiettivo:** Risoluzione malfunzionamenti hardware e configurazione driver di stampa.

### 3.1 Problemi di Rete (Stampante Offline)
1. **Verifica Segmento Rete:** Assicurarsi che l'utente sia collegato alla rete Wi-Fi `TechCorp_Corp`. Se connesso a `TechCorp_Guest`, la stampa non è autorizzata.
2. **Riavvio Spooler:** Se i documenti rimangono in coda, far eseguire il comando `net stop spooler` seguito da `net start spooler` dal prompt dei comandi come amministratore.

### 3.2 Codici Hardware Stampanti Multifunzione
In caso di segnalazione di errori sul display della stampante:
- **Codice L0 (Paper Jam):** Invitare l'utente a ispezionare il **Vassoio A** e il **Rullo Posteriore**. Non usare strumenti appuntiti.
- **Codice T1 (Toner Low):** Verificare il codice modello della cartuccia nel manuale hardware e richiedere la spedizione al magazzino.

---

## 📞 Policy di Escalation e Chiusura
- **Escalation al Livello 2:** Se il problema persiste dopo aver seguito tutti i passaggi del SOP o se richiede permessi di "Domain Admin".
- **Documentazione:** Ogni interazione deve terminare con la creazione di un ticket indicando il SOP applicato (es. "Applicato SOP-002 per Errore 505").