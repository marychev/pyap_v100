from django.conf.urls import url

from .views import BlogDetailView, BlogListView  #, LatestEntriesFeed

urlpatterns = [
    url(r'^(?P<slug>[-_\w]+)/$', BlogListView.as_view(), name='blog_index'),
    url(r'^(?P<blog_slug>[-_\w]+)/(?P<post_slug>[-_\w]+)/$',
        # r'^(?P<blog_slug>[-_\w]+)/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<slug>[-_\w]+)/$',
        BlogDetailView.as_view(),
        name='blog_detail',
        ),
    # url(r'^archive/$',
    #     BlogListView.as_view(
    #         template_name="blog/post_archive.html"),
    #         # page_template="blog/post_archive_page.html"),
    #         name="blog_archive"),
    # url(r'^latest/feed/$', LatestEntriesFeed()),
]
