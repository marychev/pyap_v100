from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from catalog.models import Catalog
from product.models import Product
from page.models import Page
from blog.models import Blog, Post
from gallery.models import Gallery


class HomeSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['home:home']

    def location(self, item):
        return reverse(item)


class GallerySitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Gallery.objects.filter(is_show=True)


class CatalogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Catalog.objects.filter(is_show=True)


class ProductSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.5

    def items(self):
        return Product.objects.filter(is_show=True)

    def lastmod(self, obj):
        return obj.updated


class BlogSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.6

    def items(self):
        return Blog.objects.filter(is_show=True)

    def lastmod(self, obj):
        return obj.updated


class PostSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Post.objects.filter(is_show=True)

    def lastmod(self, obj):
        return obj.updated


class PageSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.7

    def items(self):
        return Page.objects.filter(is_show=True)

    def lastmod(self, obj):
        return obj.updated


sitemaps = {
    'home': HomeSitemap,
    'gallery': GallerySitemap,
    'catalog': CatalogSitemap,
    'product': ProductSitemap,
    'blog': BlogSitemap,
    'post': PostSitemap,
    'page': PageSitemap,
}
