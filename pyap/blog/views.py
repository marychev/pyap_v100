from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from generic.mixins import MainPageMixin
from utils.pagination import get_pagination
from utils.leftbar import get_leftbar
from utils.next_prev_obj import get_next_prev
from .forms import CommentForm
from .models import Comment, Post, Blog
from django.contrib import messages


# class LatestEntriesFeed(Feed):
#     try:
#         site = Site.objects.get_current()
#     except:
#         site = None
#     title = "{} blog entries".format(site)
#     description = "The latest blog entries"
#     link = "/siteposts/"
#
#     def items(self):
#         return Post.objects.order_by('-created')[:5]
#
#     def item_title(self, item):
#         return item.title
#
#     def item_description(self, item):
#         return item.title


class BlogListView(MainPageMixin, TemplateView):
    """
    Блог и список его постов
    """
    template_name = 'blog/templates/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['object'] = Blog.objects.get(slug=context['slug'], is_show=True)
        context['leftbar'] = get_leftbar(Blog, context['object'])
        blog_id = context['leftbar']['root_obj'].id
        context['current_mainmenu'] = context['mainmenu'].filter(
            blog_id=blog_id, is_show=True,
        ).first()

        context['objects'] = Post.objects.filter(blog_id=context['object'].id, is_show=True).order_by('-id')
        context['objects'] = get_pagination(self.request, context['objects'])
        return context


class BlogDetailView(MainPageMixin, TemplateView):
    """
    Страница детальной информации поста. Возвращает:
    1. пост
    2. следующий и предъидущий пост
    3. форму для коментария
    4. прошедшие модерацию сообения пользователей
    5. Левую панель - список всех разделов блога
    6. Форму для коментария, отзыва - если коментарии разрешены
    """
    template_name = "blog/templates/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super(BlogDetailView, self).get_context_data(**kwargs)
        blog = get_object_or_404(Blog, slug=kwargs['blog_slug'], is_show=True)
        post = get_object_or_404(Post, slug=kwargs['post_slug'], blog_id=blog.id, is_show=True)

        initial = {
            'obj': post,
            'request': self.request,
        }
        comment_form = CommentForm(initial=initial)

        context.update({
            'post': post,
            'next_prev': get_next_prev(Post, post),
            'comment_form': comment_form,
            'comments': Comment.objects.filter(post_id=post.id, is_show=True).select_related(),
            'leftbar': get_leftbar(Blog, post.blog),
        })

        return context

    def post(self, request, *args, **kwargs):
        obj = get_object_or_404(Post, id=request.POST['post'])
        comment_form = CommentForm(request.POST, initial={'obj':obj, 'request': request})

        if comment_form.is_valid():
            comment_form.save()
            messages.success(request, ':) Сообщение отправлено!')
        else:
            messages.error(request, '(: Произошла ошибка при отправке сообщения.')
        return redirect(obj.get_absolute_url())
