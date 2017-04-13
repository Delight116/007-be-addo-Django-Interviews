# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import render, render_to_response, redirect
from django.contrib import auth
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# Create your views here.

def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)
                return redirect("/", {'username': user})
        else:
            args['login_error'] = 'Пользователь ненайден'
            return render_to_response('login.html', args)
    else:
        return render_to_response('login.html', args)


@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('/')


def registration(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            user = User.objects.get(username=newuser)
            user.is_staff = True
            user.groups.add(1)
            user.save()
            auth.login(request, newuser)
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
