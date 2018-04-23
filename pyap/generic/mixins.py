from django.views.generic.base import ContextMixin
from settings_template.models import SettingsTemplate
from cart.cart import Cart


def get_settings_template():
    """
    Получить Основную настройку которая включена.
    Если влючено больше одной, оставить только последнюю
    """
    setting_template = SettingsTemplate.objects.filter(is_included=True).first()
    return setting_template


class MainMenuMixin(ContextMixin):
    """
    Список категорий и текущим URL
    """
    def get_context_data(self, **kwargs):
        from menu.models import MainMenu
        context = super(MainMenuMixin, self).get_context_data(**kwargs)
        context['current_url'] = self.request.path
        context['mainmenu'] = MainMenu.objects._mptt_filter(is_show=True)  # .order_by('parent', 'sort')
        return context


class HomeMixin(MainMenuMixin):
    """
    Главная страница. Микис возвращает конекст:
    1. подключенную настойку шаблона.
    2. главную страницу
    3. Социальные сети приложения
    """
    def get_context_data(self, **kwargs):
        from settings_template.models import Home
        from site_info.models import SocialNetwork
        context = super(HomeMixin, self).get_context_data(**kwargs)
        context['setting_template'] = get_settings_template()
        try:
            if context['setting_template'] and context['setting_template'].home:
                context['home'] = Home.objects.get(id=context['setting_template'].home.id, is_show=True)
        except Home.DoesNotExist:
            context['home'] = []
        context['social_network'] = SocialNetwork.objects.all()
        return context


class FooterMixin(HomeMixin):
    """
    Миксин отдает футер.
    """
    def get_context_data(self, **kwargs):
        from settings_template.models import Footer
        context = super(FooterMixin, self).get_context_data(**kwargs)
        context['footer'] = Footer.objects.filter(is_show=True).first()
        return context


class MainPageMixin(FooterMixin):
    """
    Миксин обобщает основные данные для шаблона:
    1. основное меню,
    2. главная страница
    4. футер
    3. Подключаемые области
    """
    def get_context_data(self, **kwargs):
        context = super(MainPageMixin, self).get_context_data(**kwargs)
        context['request'] = self.request
        context['cart'] = Cart(self.request)
        return context

