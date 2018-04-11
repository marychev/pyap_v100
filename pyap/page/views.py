from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from generic.mixins import MainPageMixin
from utils.leftbar import get_leftbar
from blog.models import Blog
from .models import Page, PageComment
from .forms import CommentForm


class PageView(MainPageMixin, TemplateView):
    template_name = 'page/templates/page.html'

    def get_context_data(self, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['object'] = get_object_or_404(Page, slug=context['slug'])
        initial = {
            'obj': context['object'],
            'request': self.request,
        }
        comment_form = CommentForm(initial=initial)
        context['comment_form'] = comment_form
        context['leftbar'] = get_leftbar(Blog, Blog.objects.first())
        return context


class PageCommentView(MainPageMixin, TemplateView):
    """
    Коментарий к странице
    """
    model = PageComment
    form_class = CommentForm
    template_name = 'page/templates/page.html'

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Page, id=request.POST.get('page'))
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, ':) Спасибо! Отзыв принят.')
        else:
            messages.error(request, '(: Произошла ошибка при отправке отзыва.')
        return redirect(obj.get_absolute_url())
