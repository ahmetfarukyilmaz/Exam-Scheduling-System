""" from django.contrib import messages
from .models import *
from .sql import *
from .functions import *
from .forms import *
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, HttpResponse



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
    return render(request, "uploadstudentlist.html", context)


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
            schedule.school = currentAdmin.school
            schedule.name = name
            schedule.administrator = currentAdmin
            schedule.start_date = start_date
            schedule.end_date = end_date
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

def schooladmin_schedule_detail(request, id):
    form = SchoolClassForm(request.POST or None)
    schedule = Schedule.objects.get(id = id)
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
        return render(request, "schooladmin_schedule_details.html", context) """