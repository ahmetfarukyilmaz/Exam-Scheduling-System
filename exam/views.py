from django import contrib
from django.conf import settings
import os
import pandas as pd
from exam.models import *
from django.shortcuts import redirect, render, HttpResponse
from .forms import RegisterForm, LoginForm,UploadStudentForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage

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
                newTeacher.school = school
                newTeacher.save()
                login(request, newUser)
                return redirect("/teacher/")
            if school.adminAccessKey == accessKey:
                newAdministrator = SchoolAdministrator()
                newAdministrator.user = newUser
                newAdministrator.school = school
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
    for teacher in Teacher.objects.all():
        if teacher.user == user:
            return True
    return False

def is_schooladmin(user):
    if not user.is_authenticated:
        return False
    for schooladmin in SchoolAdministrator.objects.all():
        if schooladmin.user == user:
            return True
    return False


def is_student(user):
    if not user.is_authenticated:
        return False
    for student in Student.objects.all():
        if student.user == user:
            return True
    return False



@user_passes_test(is_student,"index")
def student(request):
    return render(request, "student.html")


@user_passes_test(is_teacher,'index',)
def teacher(request):
    return render(request, "teacher.html")


@user_passes_test(is_schooladmin, "index")
def schooladmin(request):
    return render(request, "schooladmin.html")

def student_viewExamDetails(request):
    return HttpResponse('Öğrenci sınav detayı görüntüleme ')


def student_changePassword(request):
    return HttpResponse('Öğrenci şifre değiştirme')

def schooladmin_uploadStudentList(request):
    return HttpResponse('Öğrenci Listesi yükleme')

def schooladmin_createSchedule(request):
    return HttpResponse('Sınav takvimi oluşturma')

def teacher_changeExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı değiştirme')

def teacher_viewExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı görüntüleme')

def checkout(request):
    return render(request, "checkout.html")

def about(request):
    return render(request, "about.html")


def schooladmin_uploadStudentList(request):
    form = UploadStudentForm(request.POST or None)
    currentAdmin = SchoolAdministrator.objects.filter(user_id=request.user.id).first()
    if form.is_valid():
        
        degree = form.cleaned_data.get('degree')
        branch = form.cleaned_data.get('branch')
        if not SchoolClass.objects.filter(school_id=currentAdmin.school.id ,degree=degree ,branch=branch).first():
            newClass = SchoolClass()
            newClass.school = currentAdmin.school
            newClass.degree = degree
            newClass.branch = branch
            newClass.save()
        else:
            newClass=SchoolClass.objects.get(school_id=currentAdmin.school.id,degree=degree,branch=branch)

        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        fs.save(uploaded_file.name,uploaded_file)
        base_dir = settings.MEDIA_ROOT
        studentList = pd.read_excel(os.path.join(base_dir,str(uploaded_file.name)),header=0,usecols="B,D,I",skiprows=3,na_filter=False,names=["Numara","Ad","Soyad"])
    
        for i in range(len(studentList)):
            if type(studentList.values[i][0])!=int:
                break
            number = studentList.values[i][0]
            firstName = studentList.values[i][1]
            lastName = studentList.values[i][2]
            if  Student.objects.filter(schoolNumber=number).first():
                continue
            newUser = User(username = firstName + "_" + str(number))
            newUser.set_password('123456')
            newUser.save()
            newStudent = Student()
            newStudent.user= newUser
            newStudent.name = str(firstName) + " " + str(lastName)
            newStudent.schoolNumber = number
            newStudent.school = currentAdmin.school
            newStudent.schoolClass = newClass
            newStudent.save()

            
    context = {
        "form" : form
    }
    return render(request, "upload.html", context)

    

