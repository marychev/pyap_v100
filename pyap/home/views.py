from django.views.generic.base import TemplateView
from generic.mixins import MainPageMixin
from generic.mixins import get_settings_template
from advertising.models import SliderHome
from product.helpers import ProductHelper


class HomePageView(MainPageMixin, TemplateView):
    template_name = 'home/templates/home.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['slider_home'] = SliderHome.objects.all()
        context['new_products'] = ProductHelper.get_new()
        context['bestseller_products'] = ProductHelper.get_bestseller()
        context['seo'] = get_settings_template()

        if context['home'].blog:
            context['posts'] = context['home'].blog.post_set.filter(is_show=True)

        return context
