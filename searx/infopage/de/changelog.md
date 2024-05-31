
# MOA vs SearXNG

MOA ist eine freie und quelloffene [Metasuchmaschine], die auf dem [SearXNG-Projekt] basiert. MOA wurde mit dem Ziel der Einfachheit und Benutzerfreundlichkeit für die Allgemeinheit entwickelt. Sie liefert gute und brauchbare Ergebnisse und gewährleistet gleichzeitig Privatsphäre, Transparenz und Freiheit im Internet.

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
  <h2>Unterschiede zwischen MOA und SearXNG</h2>
</div>

<div class="container">

<div class="moa">

<span>

<h3>MOA<template {{ "class='hide'" if get_setting('instance_customization.markdown', '') == '' else '' }}></template></h3>

- **Verbesserte Benutzeroberfläche:**
  - Neugestaltung der Benutzeroberfläche für Desktop und Mobilgeräte
  - Verbesserte Such-Infobox
  - Verbesserungen der Karten- und Bildkategorieergebnisse
  - Verbesserte Schaltfläche „Zurück zum Anfang
- **Bessere Unterstützung für Sprachen mit Schreibrichtung von rechts nach links (RTL):**
  - Verbesserte Ausrichtung der oberen Schaltflächen in der RTL-Vorlage
  - Verbesserte persische Übersetzung
- **Verbesserte Leistung und Benutzerfreundlichkeit:**
  - Langsame Motoren wurden deaktiviert, um die Geschwindigkeit zu erhöhen
  - Überarbeitete [Engine Stats] **[WIP]**
  - Suchvorschläge erscheinen nun früher
- **Zusätzliche Plugins und Funktionen:**
  - MOA Plugin Manager **[WIP]**
  - Hinzufügung des Lingva Translate Schnellreaktions-Plugins (Google Translate)
  - Hinzufügen neuer Suchmaschinen einschließlich Mastodon und Abadis
<br>  &
  - Verschiedene andere Fehlerkorrekturen

</div>

<div class="local">

{{get_setting('instance_customization.markdown','<template class="hide"></template>')}}

</div>

</div>


[Public Instances]: https://searx.space/
[Engine Stats]: {{ url_for('stats') }}
[Metasuchmaschine]: https://de.wikipedia.org/wiki/Metasuchmaschine
[SearXNG-Projekt]: https://github.com/searxng/searxng