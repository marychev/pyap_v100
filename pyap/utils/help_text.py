DESCRIPTION_HT = """"""


SORT_HT = """<br><i>
Лучше использовать за единицу сортировки 1000 или 100.. 
Так проще будет разобраться, если элементы имеют большую вложенность.<br>
Или придумайте свою систему сортировки : )
<br>ПРИМЕР - 1000:__________________ПРИМЕР - 2000:
<br>.... Пример - 1100__________________.... Пример - 2200
<br>........... пример - 1110__________________........ пример - 2220
<br>............... пример - 1111__________________............... пример - 2222</i>
"""


URL_HT = """<br><i>
<code>http://google.com</code>
Любая ссылка на веб страницу или веб-ресурс.</i>
"""


IA_CODE_HT = """<i>
Принцип работы:<br> 
<b>advantages</b> - кодовое название Включаемой облости.<br>
I.  Проинициализировать кодовое слово в ``CHOICES``(<b>advantages</b>).<br>
II. Создать HTML шаблон с кодовым словом ~/include_area/templates/<b>advantages</b>.html<br>
III. Чтобы отображать его в любом месте сайта - нужно в HTML страницы/шаблона прописать тэг:<br>
<code><small>{% get_include_area request code='<b>advantages</b>' %}</small></code>
</i>"""


SLUG_HT = """генерируется автоматически"""


SEO_TITLE_HT = """Предпочтительное значение 50-80 символов"""
SEO_DESCRIPTION_HT = """Предпочтительное значение 150-200 символов"""
SEO_KEYWORDS_HT = """Ориентируйтесь на ударные первые 150 знаков, 250 максимум"""
OG_LOCALE_HT = """
группа мета-тегов, рассказывающая социальным сетям о содержимом страниц, которыми вы делитесь.
Благодаря этому ссылки из набора символов превращаются в понятные заголовки с картинками и пояснениями.
<code>
    <meta property="og:url" content="http://www.mysite.ru/2015/02/19/arts/international/page.html" />
    <meta property="og:type" content="article" />
    <meta property="og:title" content="When Great Minds Don’t Think Alike" />
    <meta property="og:description" content="How much does culture influence creative thinking?" />
    <meta property="og:image" content="http://mysite.com/static/img/2015/02/19/img.jpg" />
</code>
"""


ROBOTS_TXT_HT = """
User-agent: Yandex\r\n
Disallow: /admin\r\n
Disallow: /dev__init\r\n
Sitemap: http://dervek.ru/sitemap.xml\r\n
Host: dervek.ru\r\n

User-agent: *\r\n
Disallow: /admin\r\n
Disallow: /dev__init\r\n
Sitemap: http://dervek.ru/sitemap.xml\r\n
Host: dervek.ru\r\n
"""

SETTINGSTEMPLATE_TYPE_LINK_HT = """
Создает CSS классы, в зависимости от выбраного типа. ``L_link``-ссылка или ``T_link``-тэг.<br>
Если выбран тип ``ссылка`` - страница будет открываться в новой вкладке. <br>
Если ``T_link`` страница будет открываться в новой вкладке!<br>
"""

SWTTINGSTEMPLATE_TITLE_HT = """
Шаблонов может быть несколько. Например, для новогодних праздников можно создать<br>
*футер<br>*главную страницу<br>*Подключить другие скрипты, ссылки и т.д.<br>
Одним словом, с помощью настроек можно создать разные варианты отображения информации : )
"""

SWTTINGSTEMPLATE_LOGO_HT = """Основной логотип сайта."""
SWTTINGSTEMPLATE_PHONE_HT = 'Например: ``8(800)-000-00-00``<br>Основной, общий номер телефона. Виден всем.'
SWTTINGSTEMPLATE_IS_INCLUDED_HT = """Включеной может быть только одина главная страница"""

SWTTINGSTEMPLATE_SCRIPTS_HT = """
Пример: "Подключение CSS фрэймворка - Bootstrap 4.0"<br>
--------------------------------------------------------<br> 
< script src="https://code.jquery.com/jquery-3.2.1.slim.min.js" integrity="sha384-KJ3o2DKtIkvYIK3UENzmM7KCkRr/rE9/Qpg6aAZGJwFDMVNA/GpGFF93hXpG5KkN" crossorigin="anonymous"></script><br>
< script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script><br>
< script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/js/bootstrap.min.js" integrity="sha384-JZR6Spejh4U02d8jOt6vLEHfe/JQGiRRSQQxSfFWpi1MquVdAyjUar5+76PVCmYl" crossorigin="anonymous"></script>
"""

SWTTINGSTEMPLATE_META_HT = """
Пример: "Подключение meta-тэга для 'Подтверждение прав на САЙТА' в Яндекс-Вебмастер"<br>
--------------------------------------------------------<br> 
< meta name="yandex-verification" content="831t65hfbfafdzyx" /><br>
Дальше можно также дописывать дугие мета-тэги.
"""

SOCIAL_NETWORK_HTML_LINK_HT = '''
Примеры некоторых иконок соц.сетей:<br> 
`````````````````````````````````````````````````<br>
``< i class="fa fa-facebook"> < /i>`` - facebook<br>
``< i class="fa fa-twitter">< /i>`` - twitter<br>
``< i class="fa fa-instagram">< /i>`` - instagram<br>
``< i class="fa fa-google-plus">< /i>`` - google-plus<br>
``< i class="fa fa-envelope">`` - envelope<br>
'''