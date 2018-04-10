from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.forms.formsets import formset_factory
from django.db import IntegrityError, transaction
from generic.mixins import MainPageMixin
from order.models import Order, OrderItem
# from review.models import ReviewProduct
from product.models import ProductComment
from .forms import LinkForm, BaseLinkFormSet, ProfileForm, NewUser, CustomAuthenticationForm
from .models import UserProfile, UserLink


def logout_view(request):
    """Выход из профиля или админки"""
    logout(request)
    return HttpResponseRedirect(reverse('home:home'))


class Login(MainPageMixin, TemplateView):
    """
    Вход на сайт
    """
    template_name = 'users/templates/login.html'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data(**kwargs)
        context['form'] = CustomAuthenticationForm()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = CustomAuthenticationForm(request, request.POST)

        if context['form'].is_valid():
            authenticated_user = authenticate(username=request.POST['username'], password=request.POST['password'])
            login(request, authenticated_user)
            return HttpResponseRedirect(reverse('home:home'))
        return render(request, self.template_name, context)


class Register(MainPageMixin, TemplateView):
    """
    Регистрация пользователя
    """
    template_name = 'users/templates/register.html'

    def get_context_data(self, **kwargs):
        context = super(Register, self).get_context_data(**kwargs)
        context['form'] = NewUser()
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['form'] = NewUser(request.POST)

        if context['form'].is_valid():
            # сохранить пол-ля и его пароль, из поля ``username`
            new_user = context['form'].save()
            profile = UserProfile.objects.create(user=new_user, phone=request.POST.get('phone'))
            profile.save()

            authenticated_user = authenticate(username=new_user.username, password=request.POST['password1'])
            login(request, authenticated_user)
            messages.success(request, u'%s, Добро пожаловать!' % request.user.username, )
            return HttpResponseRedirect(reverse('home:home'))
        return render(request, self.template_name, context)


class Profile(MainPageMixin, TemplateView):
    """
    Allows a user to update their own profile.
    """
    template_name = 'users/templates/profile.html'
    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    def get_context_data(self, **kwargs):
        context = super(Profile, self).get_context_data(**kwargs)
        user = context['request'].user
        # Get our existing link data for this user.  This is used as initial data.
        user_links = UserLink.objects.filter(user=user).order_by('anchor')
        link_data = [{'anchor': l.anchor, 'url': l.url} for l in user_links]
        context['profile_form'] = ProfileForm(user=user)
        context['link_formset'] = self.LinkFormSet(initial=link_data)
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        user = context['request'].user
        context['profile_form'] = ProfileForm(request.POST, user=user, initial={'email': user.email})
        context['link_formset'] = self.LinkFormSet(request.POST)

        if context['profile_form'].is_valid() and context['link_formset'].is_valid():
            # Save user info
            user.first_name = context['profile_form'].cleaned_data.get('first_name')
            user.last_name = context['profile_form'].cleaned_data.get('last_name')
            user.save()
            # todo: save for form development
            context['profile_form'].save()
            # Now save the data for each form in the formset
            new_links = []
            for link_form in context['link_formset']:
                anchor = link_form.cleaned_data.get('anchor')
                url = link_form.cleaned_data.get('url')
                if anchor and url:
                    new_links.append(UserLink(user=user, anchor=anchor, url=url))

            try:
                with transaction.atomic():
                    # Replace the old with the new
                    UserLink.objects.filter(user=user).delete()
                    UserLink.objects.bulk_create(new_links)
                    messages.success(request, 'Профиль обнавлен.')
            except IntegrityError:  # If the transaction failed
                messages.error(request, 'Ошибка в вашем профиле.')
            return HttpResponseRedirect(reverse('users:profile'))

        return render(request, self.template_name, context)


class Orders(MainPageMixin, TemplateView):
    """
    Все заказы пользователя в личном кабинете
    """
    template_name = 'users/templates/orders.html'
    # Create the formset, specifying the form and formset we want to use.
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    def get_context_data(self, **kwargs):
        context = super(Orders, self).get_context_data(**kwargs)
        context['orders'] = Order.objects.filter(user=context['request'].user)
        return context


class OrderDetail(MainPageMixin, TemplateView):
    """
    Детальная информация о заказе
    """
    template_name = 'users/templates/order.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, pk=context['pk'])
        context['breadcrumbs'] = [
            {'title': 'Все заказы', 'url': '/users/orders/'},
            {'title': 'Заказ {}'.format(context['pk']), 
                'url': '/users/{}/order/'.format(context['pk'])}
        ]
        return context


class ReviewProducts(MainPageMixin, TemplateView):
    """
    Все заказы пользователя в личном кабинете
    """
    template_name = 'users/templates/reviews.html'
    LinkFormSet = formset_factory(LinkForm, formset=BaseLinkFormSet)

    def get_context_data(self, **kwargs):
        context = super(ReviewProducts, self).get_context_data(**kwargs)
        # todo: [?] email: or id:
        context['review_products'] = ProductComment.objects.filter(email=self.request.user.email)
        return context
