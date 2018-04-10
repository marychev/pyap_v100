from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from filebrowser.sites import site as filebrowser_site
from django.contrib.auth import views as auth_views
from django.contrib.sitemaps.views import sitemap
from sitemap.init import sitemaps


urlpatterns = [
    url(r'^admin/filebrowser/', include(filebrowser_site.urls)),
    # url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', admin.site.urls),
    url('^', include('django.contrib.auth.urls')),

    url(r'^ckeditor/', include('ckeditor_uploader.urls')),

    url(r'^', include('home.urls', namespace='home')),
    url(r'^order/', include('order.urls', namespace='order')),
    url(r'^users/', include('users.urls', namespace='users')),
    url(r'^page/', include('page.urls', namespace='page')),
    # url(r'^review/', include('review.urls', namespace='review')),

    url(r'^blog/', include('blog.urls')),
    url(r'^gallery/', include('gallery.urls', namespace='gallery')),

    # modules
    url(r'^search/', include('search.urls', namespace='search')),
    url(r'^cart/', include('cart.urls', namespace='cart')),
    url(r'^sitemap\.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # ---- Приоритет имеет значение! ----
    url(r'^catalog/', include('catalog.urls', namespace='catalog')),
    url(r'^', include('product.urls', namespace='product')),
    url(r'^dev_init/', include('dev_init.urls')),

    # url(r'^(?P<url>[_\-\w\d]+)/$', url_hendler, name='url_handler'),
    # url(r'^defauldb/(?P<app>[_\-\w\d]+)/$', AddDefaultDB.as_view()),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)\
                   + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

