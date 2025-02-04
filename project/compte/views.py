from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db.models import *
from app.models import *
from compte.models import *
from django.contrib.auth.models import User

# Create your views here.


def connexion(request):
    if request.method == 'POST':
        usr = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(request, username=usr, password=pwd)

        if user is not None:
            login(request, user)
            return redirect('/home/')
        else:
            return redirect('/login/')
    else:
        return render(request, 'index.html')  # replace 'connexion.html' with your login form template

def deconnexion(request):
    logout(request)
    return render(request, 'logout.html')

def contact(request):
    return render(request, 'contact.html')  

def profil(request):
    return render(request, 'profile.html')