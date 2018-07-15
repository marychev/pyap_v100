from django.db import models
from filebrowser.fields import FileBrowseField
from utils.help_text import SORT_HT, IA_CODE_HT, URL_HT


class IncludeArea(models.Model):
    """
    Модель. Включаемые области текста. Предназначена для размещения постоянно повторяющегося куска HTML кода.
        Применение, в любом месте HTML кода.
            {% get_include_area request code='advantages' %}
    """
    ADVANTAGES = 'advantages'
    CODE_CHOICES = (
        (ADVANTAGES, 'Наши преимущества'),
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    is_show = models.BooleanField(default=True, verbose_name="Отображать")
    image = FileBrowseField(
        max_length=500, extensions=['.jpg', '.jpeg', '.png', '.gif'], blank=True, null=True, verbose_name='Изображение')
    description = models.TextField(verbose_name='Описание', blank=True, null=True)
    html_code = models.CharField(max_length=255, verbose_name='HTML-код', blank=True, null=True, help_text='HTML разметка с CSS')
    code = models.CharField(max_length=20, choices=CODE_CHOICES, default=ADVANTAGES, verbose_name="Код", help_text=IA_CODE_HT)
    sort = models.PositiveSmallIntegerField(default=1000, verbose_name='Сортировка', help_text=SORT_HT)
    url = models.URLField('Полный путь к веб-странице', null=True, blank=True, help_text=URL_HT)

    def __str__(self):
        return self.title

    def get_html(self):
        """
        Вернуть заполненый HTML объектами
        """
        # from django.template import Template, Context
        # template = Template('advantages.html')
        # c = Context({'include_area': self})
        # return template.render(c)

        from django.template.loader import render_to_string
        return render_to_string(self.code+'.html', {
            'include_area': IncludeArea.objects.filter(code=self.code)
        })

    class Meta:
        ordering = ('sort', 'code')
        unique_together = ('title', 'code')
        verbose_name = 'Включаемую область'
        verbose_name_plural = 'Включаемые области'
