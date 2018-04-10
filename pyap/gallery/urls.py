from django.conf.urls import url

from .views import GalleryDetailView  # GalleryDetailView,

urlpatterns = [
    url(r'^(?P<slug>[-_\w]+)/$', GalleryDetailView.as_view(), name='gallery_detail'),
]
