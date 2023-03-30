import random
import time

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse
from web import models

from django import forms

class New_ad_form(forms.ModelForm):
    class Meta:
        model = models.Ad
        fields = ['title', 'description', 'price', 'img_url']


# Create your views here.


def index(request):
    return "Index"


def log_out(request):
    rendered_reverse = HttpResponseRedirect(reverse('auth'))
    rendered_reverse.delete_cookie('token')
    return rendered_reverse


# todo Готово
def auth(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        token = time.time() + random.randint(100, 999)

        # todo проверяем на существование пользователя с такими данными, если возникла ошибка значит регистрируем пользователя
        try:
            user = models.User.objects.get(username=username, password=password)
            rendered_reverse = HttpResponseRedirect(reverse('home'))
            rendered_reverse.set_cookie('token', user.token)
            return rendered_reverse

        except Exception as e:
            print(e)
            models.User.objects.create(username=username, password=password, token=token)

            rendered_reverse = HttpResponseRedirect(reverse('home'))
            rendered_reverse.set_cookie('token', token)
            return rendered_reverse

    rendered_view = render(request, 'auth.html')
    return rendered_view


def home(request):
    token = request.COOKIES.get('token')
    # todo Проверяем авторизацию пользователя
    try:
        user = models.User.objects.get(token=token)
    except Exception as e:
        print(e)
        rendered_reverse = HttpResponseRedirect(reverse('auth'))
        return rendered_reverse

    ads = models.Ad.objects.all()
    rendered_view = render(request, 'home.html', context={'ads': ads, 'user': user})
    return rendered_view


def user(request, user_id):
    token = request.COOKIES.get('token')
    # todo Проверяем авторизацию пользователя
    try:
        user = models.User.objects.get(token=token)
    except Exception as e:
        print(e)
        rendered_reverse = HttpResponseRedirect(reverse('auth'))
        return rendered_reverse

    author = models.User.objects.get(id=user_id)

    rendered_view = render(request, 'user.html', context={
        'user': user,
        'author': author,
        'get_user_ads': author.get_user_ads
    })
    return rendered_view


def ad_edit(request, ad_id:int):

    # todo Проверяем авторизацию пользователя
    try:
        token = request.COOKIES.get('token')
        user = models.User.objects.get(token=token)
    except Exception as e:
        print(e)
        rendered_reverse = HttpResponse(reverse('auth'))
        return rendered_reverse
    message = ''

    try:
        ad = models.Ad.objects.get(id=ad_id)
        form = New_ad_form(initial={
            'title': ad.title,
            'description': ad.description,
            'price': ad.price,
            'img_url': ad.img_url
        })
    except Exception as e:
        form = New_ad_form()
        print(e)


    try:

        if request.method == "POST":
            ad = models.Ad.objects.get(id=ad_id)
            if request.FILES:
                ad.title = request.POST['title']
                ad.description = request.POST['description']
                # "" if request.POST['img_url'] == "" else ad.img_url =
                ad.img_url = request.FILES['img_url']
                ad.price = request.POST['price']
                ad.save()
            else:
                ad.title = request.POST['title']
                ad.description = request.POST['description']
                ad.img_url = ad.img_url
                ad.price = request.POST['price']
                ad.save()
            message = 'Успешно обновлено'
    except Exception as e:
        print(e)
        print(request.POST)
        print(request.FILES)
        message = 'Ошибка обновления'

    rendered_view = render(request, 'new_ad.html', context={'message': message, 'form': form, 'user': user, 'ad': ad})
    return rendered_view


def ad_new(request):
    token = request.COOKIES.get('token')
    # todo Проверяем авторизацию пользователя
    try:
        user = models.User.objects.get(token=token)
    except Exception as e:
        print(e)
        rendered_reverse = HttpResponseRedirect(reverse('auth'))
        return rendered_reverse
    message = ''

    form = New_ad_form()
    if request.method == 'POST':
        try:
            form = New_ad_form(request.POST, request.FILES, initial={'author': user})

            instance = form.save(commit=False)
            instance.author = user
            instance.save()
            if form.is_valid():
                form.save()

            message = 'Успешно!'

        except Exception as e:
            print(e)
            message = 'Не все поля заполнены'

    rendered_view = render(request, 'new_ad.html', context={'message': message, 'form': form, 'user': user, 'ad': ad})
    return rendered_view


def ad(request, ad_id):
    token = request.COOKIES.get('token')
    # todo Проверяем авторизацию пользователя
    try:
        user = models.User.objects.get(token=token)
    except Exception as e:
        print(e)
        rendered_reverse = HttpResponseRedirect(reverse('auth'))
        return rendered_reverse


    ad = models.Ad.objects.get(id=ad_id)

    rendered_view = render(request, 'ad.html', context={'ad': ad, 'user': user})
    return rendered_view
