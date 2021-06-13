""" from django.shortcuts import render
from .models import *


def student_viewSchedules(request):
    currentStudent = Student.objects.filter(user_id=request.user.id).first()
    schedules = Schedule.objects.filter(school_id=currentStudent.school_id)
    context = {
        "schedules" : schedules
    }
    return render(request, "student_schedules.html", context)

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
    return render(request, "student_schedule_details.html", context) """