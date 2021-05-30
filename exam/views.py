from django.shortcuts import render, HttpResponse
from .forms import *

# Create your views here.

def login(request):
    return render(request, "login.html")

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid:
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

    else:
        form = RegisterForm()
        context = {
        "form" : form
        }
        return render(request, "register.html", context)

    

def logout(request):
    return HttpResponse("Deneme")

def home(request):
    return HttpResponse("Home Page")

def student(request):
    return render(request, "student.html")

def teacher(request):
    return render(request, "teacher.html")

def schooladmin(request):
    return render(request, "schooladmin.html")


