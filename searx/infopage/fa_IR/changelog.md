
# MOA vs SearXNG

MOA یک [موتور فراجستجو] منبع باز و رایگان بر اساس [پروژه SearXNG] است. MOA با هدف سادگی و قابلیت استفاده برای عموم مردم، ارائه نتایج خوب و قابل استفاده در عین حصول اطمینان از حریم خصوصی، شفافیت و آزادی در اینترنت ایجاد شده است.

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

<span>

<h3>MOA<template {{ "class='hide'" if get_setting('instance_customization.markdown', '') == '' else '' }}></template></h3>

- **رابط کاربری پیشرفته:**
  - طراحی مجدد رابط کاربری دسکتاپ و موبایل
  - جعبه اطلاعات جستجوی بهبود یافته
  - بهبود نتایج دسته بندی نقشه و تصویر
  - دکمه بازگشت به بالا بهبود یافته است
- **پشتیبانی بهتر زبان از راست به چپ (RTL):**
  - تراز بهبود یافته دکمه های بالا در قالب RTL
  - ترجمه فارسی بهبود یافته
- **بهبود عملکرد و قابلیت استفاده:**
  - موتورهای کند برای افزایش سرعت غیرفعال شدند
  - بازسازی شده [Engine Stats] **[WIP]**
  - اکنون پیشنهادات جستجو زودتر ظاهر می شوند
- **افزونه ها و ویژگی های اضافی:**
  - مدیر پلاگین MOA **[WIP]**
  - اضافه شدن افزونه پاسخ سریع Lingva Translate (Google Translate)
  - اضافه شدن موتورهای جستجوی جدید از جمله Mastodon و Abadis
<br>  &
  - رفع اشکال مختلف دیگر

</div>

<div class="local">

{{get_setting('instance_customization.markdown','<template class="hide"></template>')}}

</div>

</div>


[Public Instances]: https://searx.space/
[Engine Stats]: {{ url_for('stats') }}
[موتور فراجستجو]: https://en.wikipedia.org/wiki/Metasearch_engine
[پروژه SearXNG]: https://github.com/searxng/searxng