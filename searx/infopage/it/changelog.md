
# MOA vs SearXNG

MOA è un [motore di metasearch] libero e open source basato sul [progetto SearXNG]. MOA è stato creato con l'obiettivo della semplicità e dell'usabilità per il grande pubblico, fornendo risultati validi e utilizzabili e garantendo al contempo privacy, trasparenza e libertà su Internet.

<style>
  .container {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    width: 80%;
    min-width: 350px;
    max-width: 1200px;
    margin: auto;
  }
  .container > div.moa {
    padding-right: 20px;
  }
  .container > div.local {
    border-left: 1px solid #ccc;
    padding-left: 20px;
  }
  .container > div.local:has(p > template.hide) {
    display: none;
  }
  .container > div.moa > span > h3:has(template.hide) {
    display: none;
  }
  @media (max-width: 800px) {
    .container {
      grid-template-columns: 1fr;
    }
    .container > div.local {
      border-left: 0px;
      padding-right: 20px;
    }
    .container > div.moa {
      padding-left: 20px;
    }
  }
  .container:has(div.local > p template.hide) {
    grid-template-columns: 1fr;
    width: 50%;
  }
</style>
<div style="text-align: center;">
  <h2>Differences between MOA and SearXNG</h2>
</div>

<div class="container">

<div class="moa">

<h3>MOA<template {{ "class='hide'" if get_setting('instance_customization.markdown', '') == '' else '' }}></template></h3>

- **Interfaccia utente migliorata:**
  - Riprogettazione dell'interfaccia utente desktop e mobile
  - Infobox di ricerca migliorato
  - Miglioramenti ai risultati delle categorie Mappa e Immagine
  - Pulsante di ritorno all'inizio migliorato
- **Migliore supporto della lingua da destra a sinistra (RTL):**
  - Migliorato l'allineamento dei pulsanti superiori nel modello RTL
  - Traduzione persiana migliorata
- **Prestazioni e usabilità migliorate:**
  - I motori lenti sono stati disattivati per aumentare la velocità
  - Rielaborato [Engine Stats]
  - I suggerimenti di ricerca vengono ora visualizzati prima
- **Plugin e funzionalità aggiuntive:**
  - Gestione dei plugin MOA **[WIP]**
  - L'aggiunta del plugin di risposta rapida Lingva Translate (Google Translate)
  - Aggiunti nuovi motori di ricerca, tra cui Mastodon e Abadis.
<br>  &
  - Varie altre correzioni di bug

</div>

<div class="local">

{{get_setting('instance_customization.markdown','<template class="hide"></template>')}}

</div>

</div>

[Public Instances]: https://searx.space/
[Engine Stats]: {{ url_for('stats') }}
[motore di metasearch]: https://it.wikipedia.org/wiki/Metamotore
[progetto SearXNG]: https://github.com/searxng/searxng