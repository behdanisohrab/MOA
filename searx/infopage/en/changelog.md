
# MOA vs SearXNG

MOA is a free and open source [metasearch engine] based on the [SearXNG project]. MOA was created with the aim of simplicity and usability for the general public, providing good and usable results while ensuring privacy, transparency, and freedom on the Internet.

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
  .container > div.moa > h3:has(template.hide) {
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

- **Enhanced UI/UX:**
  - Desktop & mobile user interface redesign
  - Improved search infobox
  - Map & Image category results improvements
  - Improved back to top button
- **Better RTL Language Support:**
  - Improved alignment of top buttons in RTL template
  - Improved Persian translation
- **Improved Performance & Usability:**
  - Slow engines were disabled to increase speed
  - Reworked [Engine Stats]
  - Search suggestions now appear sooner
- **Additional Plugins and Features:**
  - MOA Plugin Manager **[WIP]**
  - The addition of Lingva Translate quick response plugin (Google Translate)
  - Added new search engines including Mastodon and Abadis
<br>  &
  - Various other bug fixes

</div>

<div class="local">

{{get_setting('instance_customization.markdown','<template class="hide"></template>')}}

</div>

</div>


[Public Instances]: https://searx.space/
[Engine Stats]: {{ url_for('stats') }}
[metasearch engine]: https://en.wikipedia.org/wiki/Metasearch_engine
[SearXNG project]: https://github.com/searxng/searxng