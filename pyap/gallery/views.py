from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
# from django.views.generic.dates import DateDetailView
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from generic.mixins import MainPageMixin
from utils.pagination import get_pagination
from utils.leftbar import get_leftbar
from utils.next_prev_obj import get_next_prev

from .models import Gallery, GalleryImage


class GalleryDetailView(MainPageMixin, TemplateView):
    """
    Отобразить раздел галерею ее изображениями
    """
    template_name = 'gallery/templates/gallery.html'

    def get_context_data(self, **kwargs):
        context = super(GalleryDetailView, self).get_context_data(**kwargs)
        context['object'] = Gallery.objects.get(slug=context['slug'])
        context['leftbar'] = get_leftbar(Gallery, context['object'])
        gallery_id = context['leftbar']['root_obj'].id
        context['current_mainmenu'] = context['mainmenu'].filter(
            gallery_id=gallery_id
        ).first()

        context['objects'] = GalleryImage.objects.filter(gallery_id=context['object'])
        context['objects'] = get_pagination(self.request, context['objects'])

        return context
