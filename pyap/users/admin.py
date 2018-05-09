from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.contrib.auth.forms import UserChangeForm as DefaultUserChangeForm
from daterange_filter.filter import DateRangeFilter

from utils.abstract_admin import DefaultSettings
from .models import UserProfile, UserLink

admin.site.unregister(User)
admin.site.unregister(Group)


class UserChangeForm(DefaultUserChangeForm):
    class Meta(DefaultUserChangeForm.Meta):
        model = User


class UserProfileInline(admin.StackedInline):
    verbose_name_plural = 'Профиль'
    model = UserProfile


class UserLinkInline(admin.TabularInline):
    verbose_name = 'Ссылка'
    verbose_name_plural = 'Пользовательские ссылки'
    model = UserLink
    extra = 0
    classes = ('collapse',)


@admin.register(User)
class UserAdmin(DefaultUserAdmin, DefaultSettings):
    menu_title = "Пользователи"
    menu_group = "Пользователи"
    inlines = (UserProfileInline, UserLinkInline)
    form = UserChangeForm
    date_hierarchy = 'date_joined'
    readonly_fields = ('date_joined', 'last_login', 'password')
    search_fields = ('^username', '^email', '^last_name')
    list_filter = (
        ('date_joined', DateRangeFilter), ('last_login', DateRangeFilter),
        'is_active', 'is_staff', 'is_superuser',
    )

    list_display = ('email', 'last_name', 'is_active', 'is_staff', 'is_superuser')
    list_editable = ('is_active', 'is_staff')

    filter_horizontal = ('groups', 'user_permissions')
    fieldsets = (
        ('Основные данные', {
            'fields': (
                'username', 'first_name', 'last_name', 'email', 
                ('is_active', 'is_staff', 'is_superuser')
            )
        }),
        ('Дополнительно', {
            'fields': ('groups', 'user_permissions', 'date_joined', 'last_login'),
            'classes': ('collapse',)
        }),

    )


@admin.register(Group)
class GroupAdmin(DefaultSettings):
    menu_title = "Группы"
    menu_group = "Пользователи"

    search_fields = ('^name', 'permissions__name')
    list_filter = ('permissions', )
    filter_horizontal = ('permissions',)
