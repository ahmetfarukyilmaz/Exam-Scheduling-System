from django import contrib
from django.conf import settings
import os
from django.contrib.messages.api import success
from numpy.lib.function_base import extract
import pandas as pd
from .models import *
from .sql import *
from .functions import *
from django.shortcuts import redirect, render, HttpResponse
from .forms import *
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.crypto import get_random_string
#from .examCreatingForms import ExamForm
from django.views.generic.edit import FormView

def no_authentication(user):
    if not user.is_authenticated:
        return True
    return False


def authentication(user):
    if user.is_authenticated:
        return True
    return False

@user_passes_test(no_authentication, "logout")
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
            messages.warning(request, "Kullanıcı adı veya şifre hatalı!")
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
            messages.success(request, "Giriş Başarılı")
            return redirect("/teacher/")
        elif schooladmin is not None:
            messages.success(request, "Giriş Başarılı")
            return redirect("/schooladmin/")
        else:
            messages.success(request, "Giriş Başarılı")
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
    return redirect('index')

@user_passes_test(no_authentication, "schooladmin")
def home(request):
    return render(request, "index.html")


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



@user_passes_test(is_student,"login")
def student(request):
    return render(request, "student.html")


@user_passes_test(is_teacher,'student',)
def teacher(request):
    return render(request, "teacher.html")


@user_passes_test(is_schooladmin, "teacher")
def schooladmin(request):
    return render(request, "schooladmin.html")

# def student_viewExamDetails(request):
#     return render(request, "student_schedule_details.html")

@user_passes_test(is_student, "login")
def student_viewSchedules(request):
    currentStudent = Student.objects.filter(user_id=request.user.id).first()
    schedules = Schedule.objects.filter(school_id=currentStudent.school_id)
    context = {
        "schedules" : schedules
    }
    return render(request, "student_schedules.html", context)


@user_passes_test(is_student, "login")
def student_schedule_detail(request,id):
    schedule = Schedule.objects.get(id=id)
    exams = Exam.objects.filter(schedule_id=id)
    currentStudent = Student.objects.filter(user_id=request.user.id).first()
    students = dict()
    
    #sitting planı student a göre filtrele?
    sittingPlans = SittingPlan.objects.filter(schedule_id=id)
    for item in sittingPlans:
        if item.student == currentStudent:
            degree = item.schoolClass.degree
            branch = item.schoolClass.branch
            deskNumber = item.deskNumber

    context = {
        "schedule": schedule,
        "exams": exams,
        "students": students,
        "branch": branch,
        "degree": degree,
        "deskNumber": deskNumber,
    }
    return render(request, "student_schedule_details.html", context)



@user_passes_test(is_schooladmin, "login")
def schooladmin_schedule(request):
    currentAdmin = SchoolAdministrator.objects.get(user_id = request.user.id)
    allexams = Exam.objects.filter(ownerTeacher__school__id=currentAdmin.school_id,schedule_id=None)
    form = ScheduleForm(allexams, request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            name = form.cleaned_data.get("name")
            end_date = form.cleaned_data.get('end_date')
            start_date = form.cleaned_data.get('start_date')
            exams=form.cleaned_data.get("exams")
            schedule = Schedule()
            setSchedule(schedule,name,currentAdmin,start_date,end_date)
            schedule.save()
            for exam in exams:
                t=Exam.objects.get(pk=exam.id)
                t.schedule_id=schedule.id
                t.save()
            
            
            
            cheatingAlgorithm(request, schedule.id, currentAdmin.school_id)
            mail_sender_exam(request,schedule.id)

    schedules = Schedule.objects.filter(school_id = currentAdmin.school_id)
    context = {
        "schedules" : schedules,
        "form" : form
    }
    return render(request, "schooladmin_schedule.html", context)


@user_passes_test(is_schooladmin, "login")
def schooladmin_schedule_detail(request, id):
    schedule = Schedule.objects.get(id = id)
    degree=class_filter(schedule)[0]
    branch=class_filter(schedule)[1]
    form = SchoolClassForm(degree,branch,request.POST or None)
    exams = Exam.objects.filter(schedule_id = id)
    students = dict()
    sittingPlans = SittingPlan.objects.filter(schedule_id = id)
    if form.is_valid():
        degree = form.cleaned_data.get("degree")
        branch = form.cleaned_data.get("branch")
        for item in sittingPlans:
            if item.schoolClass.degree == degree and item.schoolClass.branch == branch:
                students[item.deskNumber] = item.student
        for i in range(1,41):
            if i not in students.keys():
                students[i] = None
        context = {
            "schedule" : schedule,
            "exams" : exams,
            "students" : students,
            "form" : form,
            "branch" : branch,
            "degree" : degree
            
        }
        return render(request, "schooladmin_schedule_details.html", context)
    
    for i in range(1,41):
        if i not in students.keys():
            students[i] = None
    context = {
        "schedule" : schedule,
        "exams" : exams,
        "students" : students,
        "form" : form,
        "branch" :"",
        "degree" :""       
    }
    return render(request, "schooladmin_schedule_details.html", context)

@user_passes_test(is_schooladmin, "login")
def schooladmin_schedule_delete(request, id):
    schedule = Schedule.objects.get(id=id)

    schedule.delete()
    messages.success(request, "Takvim Silindi")
    return redirect("schooladmin_schedule")




@user_passes_test(is_teacher, "login")
def teacher_changeExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı değiştirme')

@user_passes_test(is_teacher, "login")
def teacher_viewExamDetails(request):
    return HttpResponse('Öğretmen sınav detayı görüntüleme')


@user_passes_test(is_teacher, "login")
def teacher_exam(request):

    currentTeacher = Teacher.objects.filter(user_id=request.user.id).first()
    allClasses = SchoolClass.objects.all()
    allTeachers = Teacher.objects.all()
    class_list = []
    teacher_list = []

    for singleClass in allClasses:
        if(singleClass.school_id == currentTeacher.school_id):
              class_list.append((singleClass.id, singleClass.degree + "/" +  singleClass.branch))

    for singleTeacher in allTeachers:
        if(singleTeacher.school_id == currentTeacher.school_id):
            teacher_list.append((singleTeacher, singleTeacher.name))


    form= ExamForm(teacher_list, currentTeacher,request.POST or None)
    print("before valid")
    if form.is_valid():
        print("valid")
        name = form.cleaned_data.get('name')
        date = form.cleaned_data.get('date')
        duration = form.cleaned_data.get('duration')
        classes = form.cleaned_data.get('classes')
        examLocation = form.cleaned_data.get('examLocation')
        observerTeacherName = form.cleaned_data.get('observerTeacher')

        for teacher in allTeachers:
            if(observerTeacherName == teacher.name):
                observerTeacher = teacher

        newExam = Exam()
        newExam.name = name
        newExam.date = date
        newExam.duration =duration
        newExam.observerTeacher = observerTeacher
        newExam.ownerTeacher = currentTeacher
        newExam.save()

        for singleClass in classes:
            newExam.classes.add(singleClass)
            print(singleClass)
            students = Student.objects.filter(schoolClass_id=singleClass.id)
            for student in students :
                student.exams.add(newExam)


        messages.success(request, "Sınav oluşturuldu!")
        exams = Exam.objects.filter(ownerTeacher_id = currentTeacher.user_id)
        context = {
        "form"  : form,
        "exams" : exams
        }
        return render(request, "teacher_exam.html", context)

    exams = Exam.objects.filter(ownerTeacher_id = currentTeacher.user_id)
    context = {
        "form"  : form,
        "exams" : exams
    }

    return render(request, "teacher_exam.html", context)



def teacher_exam_delete(request, id):
    exam = Exam.objects.get(id=id)
    exam.delete()
    messages.success(request, "Sınav Silindi")
    return redirect("teacher_exam")



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


@user_passes_test(is_schooladmin, "login")
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
            newClass.numberOfStudents+=1
            print(str(newStudent.schoolNumber) + " " + newStudent.name)
            print(newClass.numberOfStudents)
        newClass.save()
        messages.success(request,degree+ "-" + branch + " sınıf listesi başarıyla yüklendi.")
        return redirect("/schooladmin/upload-student-list/")
    context = {
        "form" : form
    }
    return render(request, "upload.html", context)


@user_passes_test(authentication, "login")
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
                request.user.email=email
                request.user.save()
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
                request.user.email=email
                request.user.save()
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
                request.user.email = email
                request.user.save()
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






    


