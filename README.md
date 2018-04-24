# fsrTool
Il programma permette l'acquisizione dati da uno o più sensori FSR e traccia i 
grafici delle misurazioni. Le funzionalità principali sono due: 
1.Acquisizione dati "su richiesta" per la caratterizzazione del sensore FSR
2.Acquisizione dati in maniera continuativa 

-----------------------------
Installazione
-----------------------------
Il programma è scritto in Python2.7 ed utilizza diversi pacchetti aggiuntivi. Questi
possono essere installati tramite il file "requirements.txt" presente nella cartella 
principale:

(user)$ pip install -r requirements.txt


-----------------------------
Hardware
-----------------------------
Il programma si appoggia su:
1. Scheda Arduino Uno
2. Sensori di pressione
3. Tre resistenze da 10kOhm. 

I tre pin analogici di Arduino vengono utilizzati per leggere la tensione Vout di un 
partitore di tensione. La resistenza primaria è di 10kOhm, mentre il sensore FSR e'
la resistenza secondaria variabile.

Lo script di arduino si trova nella cartella "docs\arudino_app"


-----------------------------
File di configurazione
-----------------------------
Nella cartella "docs\src\" è presente il file di configurazione "config.py" contenente le costanti utilizzate dal programma. 

ATTENZIONE Se si cambiano i trigger di Arduino è necessario applicare le stesse modifiche
anche allo script, per poi ricaricarlo sulla scheda.


-----------------------------
1. Sensor Characterization
-----------------------------
ATTENZIONE Prima di lanciare il programma è necessario collegare la scheda al pc.

Per l'acquisizione dati è stato utilizzato un Arduino Uno. Per la funzione di 
caratterizzazione del sensore il pin di riferimento sulla scheda è l'A0, ovvero
il primo che permette l'AnalogRead().
Il programma comprende il salvataggio di un file .txt con i dati acquisiti e un
file .png con il grafico di questi. 
La cartella di Output viene creata autonomamente e i file vengono salvati nel percorso
"Output\SensorCharacterization"

1. Inserire il nome del file di Output.
2. Inserire il peso in grammi utilizzato per la caratterizzazione del sensore e premere 
   "Submit"
3. Nel terminale verrà riportato il valore di resistenza assunto dal sensore FSR in 
   corrispondenza del peso utilizzato.
4. Al termine premere "Plot" per graficare i dati ottenuti.


-----------------------------  
2. Footstep Tracker
-----------------------------
ATTENZIONE Prima di lanciare il programma è necessario collegare la scheda al pc.

La funzionalità di Footstep Tracker viene usata per ottenere un flusso continuo di dati
dai sensori FSR (in questo caso 3). I pin di riferimento su Arduino sono l'A0, A1 e A3.
Il programma comprende il salvataggio di 4 file .txt (3 con i dati acquisiti da ogni
sensore e 1 con i tre dati uniti in un unico messaggio) e 4 file .png(3 con i grafici dei
singoli sensori e 1 con i tre grafici uniti).
La cartella di Output viene creata autonomamente e i file vengono salvati nel percorso
"Output\Footstep Tracker"

1. Inserire il nome del file di Output.
2. Premere "Start" per iniziare l'acquisizione
3. Premere "Stop" per terminare l'acquisizione. I grafici vengono generati al termine 
   dell'acquisizione e vengono mostrati nella finestra inferiore che si aggiorna autonomamente
   

-----------------------------
2018 Luca Gioacchini
