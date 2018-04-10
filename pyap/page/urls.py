# -*- coding: utf-8 -*-
from django.conf.urls import url
from .views import PageView, PageCommentView


urlpatterns = [
    url(r'^(?P<slug>[_\-\w\d]+)/$', PageView.as_view(), name='page-detail'),
    url(r'^comment/page/(?P<page_id>\d+)/$', PageCommentView.as_view(), name='page_comment'),
]

