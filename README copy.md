# Estimator – Guida Rapida per Utilizzatori Non Tecnici

Questa guida spiega in modo semplice come utilizzare l’applicazione **Estimator** per generare stime basate su configurazioni personalizzate.  
Non è necessario conoscere codice o aspetti tecnici: basta seguire i passaggi.

---

## 1. Cosa fa Estimator
Estimator analizza uno o più progetti software e conta automaticamente alcuni elementi (file, componenti, occorrenze di codice).  
A ogni elemento viene associato un *peso* che rappresenta il suo impatto sulla stima finale in giorni/uomo.

Il risultato è un **report automatico** contenente:
- conteggi,
- stime,
- durata stimata in base alla dimensione del team,
- grafici e riepiloghi.

---

## 2. Creare una nuova configurazione

### 2.1 Accedi alla pagina *Create*
Dal menu principale seleziona **Crea nuova configurazione**.

La pagina è divisa in sezioni. Compila tutte le sezioni marcate come obbligatorie.

---

## 3. Sezione “Impostazioni Generali”

Compila i campi fondamentali:

### • Nome del profilo  
Un nome che identifica la configurazione (es.: *migrazione-portal*).

### • Separator width  
Ignorabile: è un parametro che influisce solo sulla larghezza delle tabelle testuali.

### • Migration factor  
Numero che moltiplica la stima finale. Utile quando si vuole includere un fattore di correzione (es.: 1.2 = +20% di stima).

### • Team sizes  
Quantità di persone coinvolte nell’attività (es.: `1,2,4`).  
Questi valori serviranno a calcolare la durata stimata in giorni.

---

## 4. Sezione “Applicazioni”

In questa sezione si elencano i progetti da analizzare.

Per ciascuno:
1. Inserisci **Nome dell’applicazione**
2. Inserisci **Percorso della cartella** sul computer
3. Premi **Aggiungi**

Ogni riga rappresenta un’app che verrà scansionata.

---

## 5. Sezione “Default Includes”

Qui si definiscono le estensioni di file che verranno considerate automaticamente.  
Gli esempi più comuni sono:

- `*.ts`
- `*.html`

Aggiungine almeno uno.

---

## 6. Sezione “Asset / Weights”

Questa è la sezione più importante.  
Serve a dire allo strumento **cosa contare** e **quanto vale** per la stima.

Ogni asset definisce una regola del tipo:  
> “Conta tutti i file che corrispondono a questo pattern, e applica loro questo peso.”

### Ogni asset contiene:

| Campo | Significato |
|-------|-------------|
| **Nome asset** | Identificatore tecnico. Unico per ogni asset. |
| **Label** | Nome breve che apparirà nei report. |
| **Enabled** | Se disattivato, l’asset non contribuisce alla stima. |
| **Mode** | Tipo di analisi:<br>• *glob*: conta file tramite wildcard (es.: `*.component.ts`)<br>• *text*: cerca occorrenze testuali nei file |
| **Pattern** | Espressione da contare:<br>• per *glob*: un wildcard<br>• per *text*: una parola o regex |
| **Include** | Lista di wildcard che limita i file da analizzare (opzionale). |
| **Peso (value)** | Quanti giorni/uomo vale una singola occorrenza del pattern. |
| **Per** | Divisore del conteggio (es.: 100 componenti con per=10 → 10 unità). |
| **oneIfAny** | Se attivo: se almeno un match è trovato, viene contato “1” invece della quantità reale. |

Dopo aver inserito i campi premi **Aggiungi asset**.  
Apparirà una tabella riassuntiva.

---

## 7. Sezione “Complexity” (opzionale)

Permette di definire un indice di complessità basato sul rapporto tra due asset.  
Se non usata, può essere lasciata vuota.

---

## 8. Salvare la configurazione

Quando tutte le sezioni sono valide, il pulsante **Salva Configurazione** diventa attivo.

Premendolo verrà generato un file `.json` che rappresenta la configurazione.

---

## 9. Eseguire una configurazione

1. Vai alla pagina **Run**.
2. Seleziona un config salvato.
3. Premi **Esegui**.

Al termine verranno prodotti:
- un output testuale,
- un file HTML completo e visualizzabile,
- il dettaglio della stima per ciascun progetto.

---

## 10. Interpretare il report

### Nel report trovi:

**• Legenda pesi:** spiega cosa è stato contato e quanto vale.  
**• Dettaglio per progetto:** mostra asset per asset cosa è stato trovato.  
**• Distribuzione stime:** evidenzia quali elementi pesano di più.  
**• Team & tempi:** indica la durata stimata per ciascun team size configurato.  
**• Complexity** (se configurata): classifica i progetti in base alle soglie impostate.

---

## 11. Domande comuni

### “Ho sbagliato un valore, devo rifare tutto?”
No: puoi riaprire la pagina *Create* e reinserire solo gli asset o i campi necessari.

### “Posso analizzare più di un progetto?”
Sì: aggiungine quanti ne desideri nella sezione Applicazioni.

### “Posso confrontare profili diversi?”
Sì: basta creare più config e rieseguirli separatamente.

---

## 12. Conclusione

Questa guida copre tutto ciò che serve per utilizzare Estimator senza competenze tecniche.  
Una volta generata la configurazione, l’analisi e il report vengono creati automaticamente.

Per una documentazione più completa (uso avanzato, formati, esempi complessi), consultare il manuale tecnico.

