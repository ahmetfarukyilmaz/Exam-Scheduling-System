from django import contrib
from exam.models import Student, Teacher, SchoolAdministrator
from django.shortcuts import redirect, render, HttpResponse
from .forms import RegisterForm, LoginForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test

# Create your views here.

def loginUser(request):
    form = LoginForm(request.POST or None)
    context = {
        "form" : form
    }

    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(username = username, password = password)
        if user is None:
            return render(request,"login.html",context)
        
        login(request, user)
        return redirect("/teacher/")

    return render(request,"login.html",context)

def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            accessKey  = form.cleaned_data.get('accessKey')
            school = form.cleaned_data.get('school')

            if school.adminAccessKey != accessKey and school.teacherAccessKey != accessKey:
                context = {
                "form" : form
                }
                messages.warning(request, "Erişim Anahtarı Hatalı")
                return render(request, "register.html", context)

            newUser = User(username = username)
            newUser.set_password(password)
            newUser.save()

            if school.teacherAccessKey == accessKey:
                newTeacher = Teacher()
                newTeacher.user = newUser
                newTeacher.save()
                login(request, newUser)
                return redirect("/teacher/")
            if school.adminAccessKey == accessKey:
                newAdministrator = SchoolAdministrator()
                newAdministrator.user = newUser
                newAdministrator.save()
                login(request, newUser)
                return redirect("/schooladmin")

            
    
    context = {
        "form" : form
    }
    return render(request, "register.html", context)
  

    

def logoutUser(request):
    logout(request)
    return redirect('index')


def home(request):
    return render(request, "homepage.html")



def is_teacher(user):
    if not user.is_authenticated:
        return False
    if user in Teacher.objects.all():
        return True
    return False

def is_schooladmin(user):
    if not user.is_authenticated:
        return False
    if user in SchoolAdministrator.objects.all():
        return True
    return False


def is_student(user):
    if not user.is_authenticated:
        return False
    if user in Student.objects.all():
        return True
    return False



@user_passes_test(is_student)
def student(request):
    return render(request, "student.html")


@user_passes_test(is_teacher,'index',)
def teacher(request):
    return render(request, "teacher.html")


@user_passes_test(is_schooladmin, "index")
def schooladmin(request):
    return render(request, "schooladmin.html")

def checkout(request):
    return render(request, "checkout.html")

def about(request):
    return render(request, "about.html")



