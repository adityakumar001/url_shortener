from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.contrib.auth.hashers import make_password, check_password
from requests.exceptions import MissingSchema
from url_shortener.forms import URLForm, UserForm
from url_shortener.models import URLModel, User
import requests as httpreq


# Create your views here.


def submit_url(request):
    session_auth = request.session is not None and request.session.get('authenticated')
    user_ = None
    urls = None

    # To get all the urls for a particular user...
    if session_auth:
        user_ = User.objects.get(email=request.session['email'])
        urls = URLModel.objects.values('id', 'timestamp', 'shortened_url', 'original_url',
                                       'userGenerated').filter(user=user_)

    if request.method == 'POST':
        urlForm = URLForm(request.POST)
        if urlForm.is_valid():
            url = URLModel()
            try:
                # This is just to check whether the url exists..
                response = httpreq.head(request.POST['original_url'])
                print(response.status_code)
            except MissingSchema as e:

                return render(request, "home.html", {'error': e.__str__().split(':')[0], 'urls': urls})

            if response.status_code is not 404:

                url.original_url = request.POST['original_url']
                url.is404 = False

                if session_auth:
                    url.user = user_

                    if 'usergenerated' in request.POST:
                        url.userGenerated = True
                        url.shortened_url = request.POST['shortened_url']
                    else:
                        url.shortened_url = shorten(request.POST['original_url'])

                else:
                    url.shortened_url = shorten(request.POST['original_url'])

                try:
                    url.save()
                    return render(request, "home.html",
                                  {'urls': urls,
                                   'url': {'original_url': url.original_url, 'short_url': url.shortened_url}})

                except IntegrityError as e:
                    return render(request, "home.html", {"error": e.__str__(), 'urls': urls})

            else:
                return render(request, "home.html", {"error": "Page does not exist!!"})

    if session_auth:
        return render(request, "home.html", {'urls': urls})

    return render(request, "home.html", {"page_title": "Tiny Me"})


def url_mapper(request):
    try:
        url = URLModel.objects.get(shortened_url=(request.get_full_path().split('/')[1]))
    except ObjectDoesNotExist as e:
        return render(request, "error_url.html")
    return redirect(url.original_url)


def register(request):
    if (request.POST):
        userForm = UserForm(request.POST)
        if userForm.is_valid():
            user = User()
            if request.POST['password'] == request.POST['repassword']:
                user.password = make_password(request.POST['password'])
                user.email = request.POST['email']
                user.name = request.POST['name']
                try:
                    user.save()
                except:
                    return render(request, "register.html",
                                  {"error": "Email already exists!!", "page_title": "Tiny Me-Register"})
            else:
                return render(request, "register.html",
                              {'error': "Password don't match!!", "page_title": "Tiny Me-Register"})
            return redirect("/")
    return render(request, "register.html", {"page_title": "Tiny Me-Register"})


def sign_in(request):
    if request.POST:
        from django.core.exceptions import ObjectDoesNotExist
        try:
            user = User.objects.get(email=request.POST['email'])
        except ObjectDoesNotExist as e:
            return render(request, "sign_in.html",
                          {'error': "Email or password incorrect!!", "page_title": "Tiny Me-Sign In"})
        if check_password(request.POST['password'], user.password):
            request.session['authenticated'] = True
            request.session['email'] = user.email
            return redirect("/")
        else:
            return render(request, "sign_in.html",
                          {"error": "Email or password incorrect!!", "page_title": "Tiny Me-Sign In"})
    return render(request, "sign_in.html", {"page_title": "Tiny Me-Sign In"})


def sign_out(request):
    request.session['authenticated'] = False
    request.session['email'] = None
    print(request.session)
    return redirect("/")


def shorten(original):
    import string
    capital_letters = list(string.ascii_uppercase)
    digits = list(string.digits)
    shuffle(capital_letters)
    shuffle(digits)

    original_ = list(original)
    original_ = list(filter(regex_filter, original_))
    shuffle(original_)

    original__ = original_[1:7]
    shuffle(original__)

    original_ = list(capital_letters[0] + digits[0])
    original__.extend(original_)
    shortened = ''.join(original__)

    try:

        URLModel.objects.get(shortened_url=shortened)
        shorten(original)

    except ObjectDoesNotExist:
        return shortened


def shuffle(list_to_shuffle):
    import random
    random.shuffle(list_to_shuffle)
    random.shuffle(list_to_shuffle)
    random.shuffle(list_to_shuffle)


def regex_filter(original):
    import re
    return re.match(r'[A-Za-z0-9]', original) is not None


def delete_url(request):
    short_url = request.GET['shortened_url']
    if short_url and request.session and request.session['authenticated']:
        URLModel.objects.get(shortened_url=short_url).delete()
    return redirect("/")
