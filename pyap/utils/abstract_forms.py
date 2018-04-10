from django import forms
from .client import get_client_ip


class ABSCommentForm(forms.ModelForm):
    """
    Абстрактная форма Отзыва/коментария/вопроса/ для пользователя.
    """
    def __init__(self, *args, **kwargs):
        super(ABSCommentForm, self).__init__(*args, **kwargs)
        user = None
        username = None
        email = None
        # default initialisation
        self.fields['user'].widget = forms.HiddenInput()
        self.fields['username'].widget = forms.HiddenInput()
        self.fields['ip_address'].widget = forms.HiddenInput()

        if 'initial' in kwargs.keys():
            request = kwargs['initial']['request']
            self.fields['ip_address'].initial = get_client_ip(request)
            # зарегистрированый пользователь
            if request.user.is_authenticated:
                user = request.user
                username = user.username if user.is_authenticated() else username
                email = user.email if user.is_authenticated() else email

        self.fields['user'].initial = user
        self.fields['username'].initial = username
        self.fields['email'].initial = email

