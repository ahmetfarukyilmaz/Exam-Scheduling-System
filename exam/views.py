from django import contrib
from django.conf import settings
import os
from numpy.lib.function_base import extract
import pandas as pd
from exam.models import *
from exam.sql import *
from exam.functions import *
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.core.files.storage import FileSystemStorage
from django.utils.crypto import get_random_string
from django.core.mail import send_mail
from django.template.loader import render_to_string
#from .examCreatingForms import ExamForm

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
        try:
            teacher =Teacher.objects.get(user_id = request.user.id)
        except Teacher.DoesNotExist:
            teacher = None
        try:
            schooladmin =SchoolAdministrator.objects.get(user_id = request.user.id)
        except SchoolAdministrator.DoesNotExist:
            schooladmin = None

        if teacher is not None:
            return redirect("/teacher/")
        elif schooladmin is not None:
            return redirect("/schooladmin/")
        else:
            return redirect("/student/")

        
    return render(request,"login.html",context)


def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            accessKey  = form.cleaned_data.get('accessKey')
            school = form.cleaned_data.get('school')

            if User.objects.filter(username=username).exists():
                context = {
                "form" : form
                }
                messages.warning(request, "Bu Kullanıcı Adı Mevcut")
                return render(request, "register.html", context)
        
            if school.adminAccessKey != accessKey and school.teacherAccessKey != accessKey:
                context = {
                "form" : form
                }
                messages.warning(request, "Erişim Anahtarı Hatalı!")
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
                messages.success(request,"Başarıyla Kayıt Oldunuz!")
                return redirect("/teacher/")
            if school.adminAccessKey == accessKey:
                newAdministrator = SchoolAdministrator()
                newAdministrator.user = newUser
                newAdministrator.school = school
                newAdministrator.save()
                login(request, newUser)
                messages.success(request,"Başarıyla Kayıt Oldunuz!")
                return redirect("/schooladmin")

            
    
    context = {
        "form" : form
    }
    return render(request, "register.html", context)
  

    

def logoutUser(request):
    logout(request)
    messages.success(request, "Başarıyla Çıkış Yaptınız!")
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


#@user_passes_test(is_teacher,'index',)
def teacher(request):
    return render(request, "teacher.html")


#@user_passes_test(is_schooladmin, "index")
def schooladmin(request):
    return render(request, "schooladmin.html")

def student_viewExamDetails(request):
    return HttpResponse('Öğrenci sınav detayı görüntüleme ')


def student_changePassword(request):
    return HttpResponse('Öğrenci şifre değiştirme')

def schooladmin_createSchedule(request):
    return HttpResponse('Sınav takvimi oluşturma')

def teacher_changeExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı değiştirme')

def teacher_viewExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı görüntüleme')

def teacher_createExam(request):
    form = ExamForm(request.POST)
    context = {
        'form' : form
    }

    return render(request, "createExam.html", context)

def registerSchool(request):
    form = registerSchoolForm(request.POST or None)
    if form.is_valid():
        schoolName = form.cleaned_data.get('schoolName')
        email = form.cleaned_data.get('email')
        phoneNumber = form.cleaned_data.get('phoneNumber')
        country = form.cleaned_data.get('country')
        city = form.cleaned_data.get('city')
        province = form.cleaned_data.get('province')
        street = form.cleaned_data.get('street')
        postalCode = form.cleaned_data.get('postalCode')
        address = Address()
        setAddress(address,country,city,province,street,postalCode)
        address.save()
        newSchool = School()
        adminAccessKey=get_random_string(length=18)
        teacherAccessKey=get_random_string(length=18)
        setSchool(newSchool,schoolName,address,email,phoneNumber,adminAccessKey,teacherAccessKey)
        newSchool.save()
        mail_sender(email,teacherAccessKey,adminAccessKey)
        messages.success(request,'Okul Kaydetme Başarılı. Mail adresinize gelen erişim anahtarları ile sisteme kayıt olabilirsiniz.')
        return redirect('/register-school/')
    context = {
        'form': form
    }
    return render(request, "registerschool.html",context)

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

        studentList = read_student_list(request)

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
            print(str(newStudent.schoolNumber) + " " + newStudent.name)
            

        messages.success(request,degree+ "-" + branch + " sınıf listesi başarıyla yüklendi.")
        return redirect("/schooladmin/upload-student-list/")
    context = {
        "form" : form
    }
    return render(request, "upload.html", context)



def profile(request):
    try:
        teacher =Teacher.objects.get(user_id = request.user.id)
    except Teacher.DoesNotExist:
        teacher = None
    try:
        schooladmin =SchoolAdministrator.objects.get(user_id = request.user.id)
    except SchoolAdministrator.DoesNotExist:
        schooladmin = None
    try:
        student =Student.objects.get(user_id = request.user.id)
    except Student.DoesNotExist:
        student = None

    if(teacher is not None):
        if request.method == "POST":
            form = TeacherInfoForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phoneNumber = form.cleaned_data.get('phoneNumber')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                province = form.cleaned_data.get('province')
                street = form.cleaned_data.get('street')
                postalCode = form.cleaned_data.get('postalCode')
                if teacher.address != None:
                    address = teacher.address
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                else:
                    address = Address()
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                    teacher.address = address
                    teacher.save()
                teacher.name = name
                teacher.email = email
                teacher.phoneNumber = phoneNumber
                teacher.save()
                context = {
                    "form" : form
                }
                messages.success(request, "Başarılı!")
                return render(request, "profile.html", context)

            context = {
                "form" : form
            }
            return render(request, "profile.html", context)
        else:
            if teacher.address == None:
                dict = {
                    "name" : teacher.name,
                    "email" : teacher.email,
                    "phoneNumber" : teacher.phoneNumber
                    
                }
            else:
                dict = {
                    "name" : teacher.name,
                    "email" : teacher.email,
                    "phoneNumber" : teacher.phoneNumber,
                    "country" : teacher.address.country,
                    "city"    : teacher.address.city,
                    "province": teacher.address.province,
                    "street"  : teacher.address.street,
                    "postalCode" : teacher.address.postalCode
                }
            form = TeacherInfoForm(dict)
            
            
            context = {
                "form" : form
            }
            return render(request, "profile.html", context)
    
    if(schooladmin is not None):
        schooladmin =SchoolAdministrator.objects.get(user_id = request.user.id)
        if request.method == "POST":
            form = SchoolAdminInfoForm(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                phoneNumber = form.cleaned_data.get('phoneNumber')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                province = form.cleaned_data.get('province')
                street = form.cleaned_data.get('street')
                postalCode = form.cleaned_data.get('postalCode')
                if schooladmin.address != None:
                    address = schooladmin.address
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                else:
                    address = Address()
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                    schooladmin.address = address
                    schooladmin.save()
                schooladmin.name = name
                schooladmin.email = email
                schooladmin.phoneNumber = phoneNumber
                schooladmin.save()
                context = {
                    "form" : form
                }
                messages.success(request, "Başarılı")
                return render(request, "profile.html", context)

            context = {
                "form" : form
            }
            return render(request, "profile.html", context)
        else:
            if schooladmin.address == None:
                dict = {
                    "name" : schooladmin.name,
                    "email" : schooladmin.email,
                    "phoneNumber" : schooladmin.phoneNumber
                    
                }
            else:
                dict = {
                    "name" : schooladmin.name,
                    "email" : schooladmin.email,
                    "phoneNumber" : schooladmin.phoneNumber,
                    "country" : schooladmin.address.country,
                    "city"    : schooladmin.address.city,
                    "province": schooladmin.address.province,
                    "street"  : schooladmin.address.street,
                    "postalCode" : schooladmin.address.postalCode
                }
            form = SchoolAdminInfoForm(dict)
            
            
            context = {
                "form" : form
            }
            return render(request, "profile.html", context)
    
    if(student is not None):
        student =Student.objects.get(user_id = request.user.id)
        if request.method == "POST":
            form = StudentInfoForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data.get('email')
                phoneNumber = form.cleaned_data.get('phoneNumber')
                country = form.cleaned_data.get('country')
                city = form.cleaned_data.get('city')
                province = form.cleaned_data.get('province')
                street = form.cleaned_data.get('street')
                postalCode = form.cleaned_data.get('postalCode')
                if student.address != None:
                    address = student.address
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                else:
                    address = Address()
                    setAddress(address,country,city,province,street,postalCode)
                    address.save()
                    student.address = address
                    student.save()
                student.email = email
                student.phoneNumber = phoneNumber
                student.save()
                context = {
                    "form" : form
                }
                messages.success(request, "Başarılı")
                
            context = {
                "form" : form
            }
            return render(request, "profile.html", context)
            
        else:
            if student.address == None:
                dict = {
                    "email" : student.email,
                    "phoneNumber" : student.phoneNumber
                    
                }
            else:
                dict = {
                    "email" : student.email,
                    "phoneNumber" : student.phoneNumber,
                    "country" : student.address.country,
                    "city"    : student.address.city,
                    "province": student.address.province,
                    "street"  : student.address.street,
                    "postalCode" : student.address.postalCode
                }
            form = StudentInfoForm(dict)
            
            
            context = {
                "form" : form
            }
            return render(request, "profile.html", context)

    


    




    


