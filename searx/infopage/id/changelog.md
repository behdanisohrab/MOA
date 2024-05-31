
# MOA vs SearXNG

MOA adalah mesin pencari [metasearch] yang gratis dan bersifat open source yang didasarkan pada [proyek SearXNG]. MOA dibuat dengan tujuan kesederhanaan dan kegunaan untuk masyarakat umum, memberikan hasil yang baik dan dapat digunakan sambil memastikan privasi, transparansi, dan kebebasan di Internet.

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
  <h2>Perbedaan antara MOA dan SearXNG</h2>
</div>

<div class="container">

<div class="moa">

<h3>MOA<template {{ "class='hide'" if get_setting('instance_customization.markdown', '') == '' else '' }}></template></h3>

- **Antarmuka Pengguna yang Disempurnakan:**
  - Desain ulang antarmuka pengguna desktop & seluler
  - Kotak informasi pencarian yang lebih baik
  - Peningkatan hasil kategori Peta & Gambar
  - Tombol kembali ke atas yang lebih baik
- **Dukungan Bahasa dari kanan ke kiri (RTL) yang lebih baik:**
  - Penyelarasan tombol atas yang lebih baik dalam templat RTL
  - Terjemahan bahasa Persia yang lebih baik
- **Peningkatan Kinerja & Kegunaan:**
  - Mesin lambat dinonaktifkan untuk meningkatkan kecepatan
  - Pengerjaan Ulang [Engine Stats] **[WIP]**
  - Saran pencarian sekarang muncul lebih cepat
- **Plugin dan Fitur Tambahan:**
  - Manajer Plugin MOA **[WIP]**
  - Penambahan plugin respons cepat Lingva Translate (Google Translate)
  - Menambahkan mesin pencari baru termasuk Mastodon dan Abadis
<br>  &
  - Berbagai perbaikan bug lainnya

</div>

<div class="local">

{{get_setting('instance_customization.markdown','<template class="hide"></template>')}}

</div>

</div>


[Public Instances]: https://searx.space/
[Engine Stats]: {{ url_for('stats') }}
[metasearch]: https://en.wikipedia.org/wiki/Metasearch_engine
[proyek SearXNG]: https://github.com/searxng/searxng