""" from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
from .forms import *


def teacher_createExam(request):

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
    if form.is_valid():
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


        for singleExamLocation in examLocation:
            newExam.examLocation.add(singleExamLocation)


        messages.success(request, "Sınav oluşturuldu!")
        return redirect("/teacher/")

    context = {
        "form": form
    }

    return render(request, "createExam.html", context) """