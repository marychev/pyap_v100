# -*- coding: utf-8 -*-
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import validate_email
from django.forms.formsets import BaseFormSet
from django.contrib.auth.forms import authenticate, UsernameField
from django.utils.translation import ugettext_lazy as _
from .models import UserProfile, User


class CustomAuthenticationForm(forms.Form):
    """
    Base class for authenticating users. Extend this to get a form that accepts
    username/password logins.
    """
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={'autofocus': True}),
    )
    password = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput,
    )

    error_messages = {
        'invalid_login': _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        'inactive': _("This account is inactive."),
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        The 'request' parameter is set for custom auth use by subclasses.
        The form data comes in via the standard 'data' kwarg.
        """
        self.request = request
        self.user_cache = None
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs)

        # Set the label for the "username" field.
        self.username_field = User._meta.get_field(User.USERNAME_FIELD)
        if self.fields['username'].label is None:
            self.fields['username'].label = 'Email'

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Controls whether the given User may log in. This is a policy setting,
        independent of end-user authentication. This default behavior is to
        allow login by active users, and reject login by inactive users.

        If the given user cannot log in, this method should raise a
        ``forms.ValidationError``.

        If the given user may log in, this method should return None.
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache


class NewUser(UserCreationForm):
    """Создание нового пользователя"""

    def __init__(self, *args, **kwargs):
        super(NewUser, self).__init__(*args, **kwargs)
        self.fields['username'].label = 'Email'

    class Meta:
        model = User
        fields = ("username",)
        field_classes = {'username': forms.EmailField}

    def clean_email(self):
        # TODO: неизвестный метод
        try:
            email = validate_email(self.cleaned_data.get("email"))
            self.instance.email = self.cleaned_data.get('email')
        except forms.ValidationError:
            raise ('|x_x|: ERROR {0} {1}'.format(self.__class__.__name__, self.errors), )
        return email

    def save(self, commit=True):
        user = super(NewUser, self).save(commit=commit)
        user.email = user.username
        if commit:
            user.save()
        return user


class LinkForm(forms.Form):
    """Форма для отдельных пользовательских ссылок"""
    anchor = forms.CharField(
        max_length=100, required=False,
        widget=forms.TextInput(attrs={'placeholder':  ':Название', 'class': 'form-control'}), )
    url = forms.URLField(
        required=False, widget=forms.URLInput(attrs={'placeholder': ':URL / полнуй путь к странице', 'class': 'form-control'}))


class ProfileForm(forms.Form):
    """
    Form for user to update their own profile details
    (excluding links which are handled by a separate formset)
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(ProfileForm, self).__init__(*args, **kwargs)

        try:
            patronymic = self.user.userprofile.patronymic
            phone = self.user.userprofile.phone
            birthday = self.user.userprofile.birthday
            address = self.user.userprofile.address
        except UserProfile.DoesNotExist:
            patronymic = None
            phone = None
            birthday = None
            address = None

        self.fields['first_name'] = forms.CharField(
            max_length=30, label='Имя*', initial=self.user.first_name,
            widget=forms.TextInput(attrs={'placeholder': ':Имя', 'class': 'form-control'}))
        self.fields['last_name'] = forms.CharField(
            max_length=30, label='Фамилия*', initial=self.user.last_name,
            widget=forms.TextInput(attrs={'placeholder': ':Фамилия', 'class': 'form-control'}))
        self.fields['patronymic'] = forms.CharField(
            max_length=30, label='Отчество', initial=patronymic, required=False,
            widget=forms.TextInput(attrs={'placeholder': ':Отчество', 'class': 'form-control'}))
        self.fields['phone'] = forms.CharField(
            max_length=30, label='Телефон*', initial=phone,
            widget=forms.TextInput(attrs={'placeholder': ':Телефон', 'class': 'form-control jsPhoneInput'}))
        self.fields['birthday'] = forms.DateField(
            label='День рождения', initial=birthday, required=False,
            widget=forms.DateInput(attrs={'placeholder': ':День рождения', 'class': 'form-control jsDatepicker'}))
        self.fields['address'] = forms.CharField(
            max_length=512, label='Адрес', initial=address, required=False,
            widget=forms.TextInput(attrs={'placeholder': ':Адрес', 'class': 'form-control'}))

    def save(self):
        birthday = None
        if self.cleaned_data['birthday']:
            str_birthday = str(self.cleaned_data['birthday']).replace('.', '-')
            birthday = datetime.datetime.strptime(str_birthday, "%Y-%m-%d").date()

        UserProfile.objects.update_or_create(
            user=self.user,
            defaults={
                'patronymic': self.cleaned_data['patronymic'],
                'phone': self.cleaned_data['phone'],
                'birthday': birthday,
                'address': self.cleaned_data['address']
                })


class BaseLinkFormSet(BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        anchors = []
        urls = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                anchor = form.cleaned_data['anchor']
                url = form.cleaned_data['url']

                # Check that no two links have the same anchor or URL
                if anchor and url:
                    if anchor in anchors:
                        duplicates = True
                    anchors.append(anchor)

                    if url in urls:
                        duplicates = True
                    urls.append(url)

                if duplicates:
                    raise forms.ValidationError('Ссылки должны иметь уникальные наименования и URL-адреса.', code='duplicate_links')
                # Check that all links have both an anchor and URL
                if url and not anchor:
                    raise forms.ValidationError('Все ссылки должны иметь наименование.', code='missing_anchor')
                elif anchor and not url:
                    raise forms.ValidationError('Все ссылки должны иметь URL-адрес.', code='missing_URL')


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  HELPFUL
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# class UserProfileForm(forms.ModelForm):
#     """
#     Форма для пользователя, чтобы обновить свои собственные данные профиля
#     (исключая ссылки, которые обрабатываются отдельной формой)
#     """
#     # def __init__(self, *args, **kwargs):
#     #     # magic
#     #     self.user = kwargs['instance'].user
#     #     user_kwargs = kwargs.copy()
#     #     user_kwargs['instance'] = self.user
#     #     self.user_form = UserProfileForm(*args, **user_kwargs)
#     #     # magic end
#     #
#     #     super(UserProfileForm, self).__init__(*args, **kwargs)
#     #
#     #     self.fields.update(self.user_form.fields)
#     #     self.initial.update(self.user_form.initial)
#     #     # self.user = kwargs.pop('user', None)
#
#     first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     patronymic = forms.CharField(required=False, label='Отчество', widget=forms.TextInput(attrs={'class': 'form-control'}))
#     birthday = forms.DateField(label='День рождения', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}))
#     phone = forms.CharField(label='Телефон', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+7(888)-88-88'}))
#     address = forms.CharField(
#         label='Адрес', widget=forms.TextInput(attrs={'class': 'form-control'}),
#         help_text='Адрес по умолчанию, для доставки товара.')
#
#     class Meta:
#         model = UserProfile
#         fields = ('first_name', 'last_name', 'patronymic', 'birthday', 'phone', 'address')
#
#     def save(self, user=None, request=None):
#         user_profile = super(UserProfileForm, self).save(commit=False)
#         if user:
#             user_profile.user = user
#             # user_profile.phone = request.POST.get('phone', '')
#         user_profile.save()
#         return user_profile