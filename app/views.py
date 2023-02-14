from django.shortcuts import render

# Create your views here.
from app.forms import *
from django.http import HttpResponse

def home(request):
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


        