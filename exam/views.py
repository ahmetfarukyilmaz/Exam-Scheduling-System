from django.shortcuts import render, HttpResponse

# Create your views here.

def login(request):
    return render(request, "login.html")

def register(request):
    return render(request, "register.html")

def logout(request):
    return HttpResponse("Deneme")

def student(request):
    return render(request, "student.html")

def teacher(request):
    return render(request, "teacher.html")

def schooladmin(request):
    return render(request, "schooladmin.html")


