from utils.abstract_forms import ABSCommentForm
from .models import Comment
from django import forms


class CommentForm(ABSCommentForm):
    """
    Форма Коментария для пользователя
    """
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['post'].widget = forms.HiddenInput()
        # инициализируем объект для формы(абстрактной)
        if 'initial' in kwargs.keys():
            obj = kwargs['initial']['obj']
            self.fields['post'].initial = obj

    class Meta:
        model = Comment
        exclude = ('is_show',)
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
