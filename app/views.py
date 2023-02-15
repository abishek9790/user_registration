from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required


def home(request):
    if request.session.get('username'):
        username=request.session.get('username')
        d={'username':username}
        return render(request, 'home.html',d)
    return render(request, 'home.html')


def register(request):
    uf=userform()
    pf=profileform()
    d={'uf':uf,'pf':pf}

    if request.method=='POST' and request.FILES:
        ufo=userform(request.POST)
        pfo=profileform(request.POST,request.FILES)
        if ufo.is_valid() and pfo.is_valid():
            ufd=ufo.save(commit=False)
            password=ufo.cleaned_data['password']
            ufd.set_password(password)
            ufd.save()

            pfd=pfo.save(commit=False)
            pfd.profile_user=ufd
            pfd.save()

            return HttpResponse("registration is successfully")
    return render(request, 'register.html',d)

def user_login(request):
    if request.method=='POST':
        username=request.POST['un']
        password=request.POST['pw']
        user=authenticate(username=username,password=password)
        if user and user.is_active:
            login(request, user)
            request.session['username']=username
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponse("you are not an user")
    return render(request, 'user_login.html')

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
