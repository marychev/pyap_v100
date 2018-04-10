from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from utils.abstract_model import ABSContentModel, ABSImageModel, ABSCommentModel
from mptt.models import MPTTModel, TreeForeignKey
from users.models import User
from .signals import save_comment


class Blog(MPTTModel, ABSContentModel):
    """
    Блок. Включает в себю множество постов :model:`blog.Post`.
    """
    parent = TreeForeignKey(
        'self', null=True, related_name='subitems', blank=True, db_index=True, verbose_name='Родительский блог',
        on_delete=models.SET_NULL)
    author = models.ForeignKey(User, verbose_name='Автор',blank=True, null=True)

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = BlogImage.objects.filter(blog_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return BlogImage.objects.filter(blog_id=self.id)

    def get_absolute_url(self):
        kwargs = {
            'slug': self.slug,
            # 'year': '%04d' % self.created.year,
            # 'month': '%02d' % self.created.month,
            # 'day': '%02d' % self.created.day,
        }
        return reverse('blog_index', kwargs=kwargs)
    # -----------------------------------------------------------------------------------

    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        unique_together = ('title', 'parent', 'slug')

    class MPTTMeta:
        order_insertion_by = ('parent', 'sort')


class BlogImage(ABSImageModel):
    """
    Фотографии для раздела Блога :model:`blog.Blog`.
    """
    blog = models.ForeignKey(Blog, verbose_name='Блог')

    def __str__(self):
        return self.blog.title

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'


class Post(ABSContentModel):
    """
    Посты для блога
    """
    blog = models.ForeignKey(Blog, verbose_name='Блог', blank=True, null=True, on_delete=models.SET_NULL)
    author = models.ForeignKey(User, verbose_name='Автор', null=True, blank=True, on_delete=models.SET_NULL)
    is_allow_comments = models.BooleanField(default=True, verbose_name='разрешить комментарии')
    comment_count = models.IntegerField(blank=True, default=0, verbose_name='Кол-во коментариев')

    # ---------------------------------------------------------------------------------
    # [!] Повторяются методы, если у модельи есть привязка к модели его фотографий ---
    # ---------------------------------------------------------------------------------
    def get_main_image(self):
        """
        Если модель имеет фотографии то этот метод должен быть!
        Вернуть главную, или 1ю.
        """
        images = PostImage.objects.filter(post_id=self.id)
        if images:
            image = images.first()
            if images.filter(image_is_main=True).exists():
                image = images.filter(image_is_main=True).first()
            return image

    def get_images(self):
        """
        Вернуть все фотографии объекта
        """
        return PostImage.objects.filter(post_id=self.id)
    # -----------------------------------------------------------------------------------

    def get_absolute_url(self):
        kwargs = {
            'blog_slug': self.blog.get_root().slug,
            'post_slug': self.slug,
        }
        return reverse('blog_detail', kwargs=kwargs)

    class Meta:
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'
        ordering = ('blog', 'sort', 'is_show')


class PostImage(ABSImageModel):
    """
    Фотографии для Поста :model:`blog.Post`.
    """
    post = models.ForeignKey(Post, verbose_name='Пост')

    def save(self, *args, **kwargs):
        self.set_image_title(obj=self.post)
        super(PostImage, self).save(*args, **kwargs)

    class Meta:
        verbose_name = 'Фотографию'
        verbose_name_plural = 'Фотографии'


class Comment(ABSCommentModel):
    """
    Коментарии к посту
    """
    post = models.ForeignKey(Post, verbose_name='Пост', null=True, on_delete=models.SET_NULL)


post_save.connect(save_comment, sender=Comment)
