# Donation with Amazon
Effettua i tuoi su Amazon normalmente usando questi link referenziati, le commissioni pubblicitarie verranno devolute in beneficienza alla fondazione Onlus scelta dall'utente.

## Funzionamento del sito
Accedendo al sito www.donationwithamazon.it, si può inserire un link ad un prodotto Amazon nel box scegliere poi la fondazione Onlus che si desidera sostenere.
Viene fatta una chiamata HTTP con metodo POST e viene elaborata la richiesta, cercando il prodotto su Amazon.it
Nel caso di esito positivo viene restituito un link referenziato, altrimenti una pagina di errore.

## Funzionamento del bot
Avviando il bot l'utente si registra e salva le fondazioni Onlus di suo interesse. Ogni volta che manderà un messaggio, verrà controllata la presenza di un link Amazon e si tenterà la ricerca del prodotto. In caso di esito positivo, il bot risponde con un'anteprima del prodotto e il link referenziato.