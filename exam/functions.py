import os
from django.conf import settings
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
import pandas as pd
from .models import *
from django.shortcuts import redirect, render
import math
from .forms import *
from .sql import *



def mail_sender(email,teacherAccessKey,adminAccessKey):
    template = render_to_string('email.html',
    {'teacherAccessKey':teacherAccessKey,
    'adminAccessKey':adminAccessKey})
    send_mail('Exam Scheduling System Erişim Anahtarları',
    template,settings.EMAIL_HOST_USER,
    [str(email)],fail_silently=False)



def mail_sender_exam(request,schedule_id):
    students = Student.objects.distinct().filter(exams__schedule_id=schedule_id)
    for student in students:
        email=User.objects.get(id=student.user_id).email
        schedule = Schedule.objects.get(pk=schedule_id)
        exams = student.exams.filter(schedule_id=schedule_id)
        template = render_to_string('emailexam.html',
        {'exams':exams,
        'schedule':schedule})
        send_mail('Sınav Bilgilendirme',
        template,settings.EMAIL_HOST_USER,
        [email],fail_silently=False)
        if email:
            print(student.name + " öğrencisine mail gönderildi")
    


def read_student_list(request):
    uploaded_file = request.FILES['document']
    fs = FileSystemStorage()
    fs.save(uploaded_file.name,uploaded_file)
    base_dir = settings.MEDIA_ROOT
    return pd.read_excel(os.path.join(base_dir,str(uploaded_file.name)),
        header=0,usecols="B,D,I",skiprows=3,na_filter=False,names=["Numara","Ad","Soyad"])


def cheatingAlgorithm(request, schedule_id, school_id):
    students= Student.objects.filter(exams__schedule_id=schedule_id)
    schedule = Schedule.objects.get(id=schedule_id)
    numberofStudents = students.count()
    classes  = SchoolClass.objects.filter(school_id=school_id)
    numberOfClasses = classes.count()
    print("Öğrenci sayısı:" + str(numberofStudents))
    print("Sınıf sayısı:" + str(numberOfClasses))
    nineGrades=students.distinct().filter(schoolClass__degree=9)
    nineGradesCount = nineGrades.count()
    tenGrades = students.distinct().filter(schoolClass__degree=10)
    tenGradesCount = tenGrades.count()
    elevenGrades = students.distinct().filter(schoolClass__degree=11)
    elevenGradesCount = elevenGrades.count()
    twelveGrades = students.distinct().filter(schoolClass__degree=12)
    twelveGradesCount=twelveGrades.count()
    maxCount=max(nineGradesCount,tenGradesCount,elevenGradesCount,twelveGradesCount)
    studentPerClass=math.ceil((maxCount*4)/numberOfClasses)
    print("Sınıf başına düşen öğrenci:" + str(studentPerClass))
    print("9. sınıf: " + str(nineGradesCount))
    print("10. sınıf: " + str(tenGradesCount))
    print("11. sınıf: " + str(elevenGradesCount))
    print("12. sınıf: "+  str(twelveGradesCount))
    nine,ten,eleven,twelve,c,perDesk=0,0,0,0,0,4
    completed = 0
    for student in nineGrades:
        print(student.name)
    for schoolClass in classes:
        for x in range(40):
            if completed>0:
                perDesk=perDesk-completed
            if perDesk==4:
                if x%perDesk==0  and nine<nineGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,nineGrades[nine],x+1)
                    nine+=1
                    sittingplan.save()
                    c+=1
                    if nine==nineGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))
                elif x%perDesk==1 and ten<tenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,tenGrades[ten],x+1)
                    ten+=1
                    sittingplan.save()
                    c+=1
                    if ten==tenGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))
                elif x%perDesk==2 and eleven<elevenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,elevenGrades[eleven],x+1)
                    eleven+=1
                    sittingplan.save()
                    c+=1
                    if eleven==elevenGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))  
                elif x%perDesk==3 and twelve<twelveGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,twelveGrades[twelve],x+1)
                    twelve+=1
                    sittingplan.save()
                    c+=1
                    if twelve==twelveGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))

            elif perDesk==3:
                if x%perDesk==0 and nine<nineGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,nineGrades[nine],x+1)
                    nine+=1
                    sittingplan.save()
                    c+=1
                    if nine==nineGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))
                elif x%perDesk==1 and ten<tenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,tenGrades[ten],x+1)
                    ten+=1
                    sittingplan.save()
                    c+=1
                    if ten==tenGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))
                elif x%perDesk==2 and eleven<elevenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,elevenGrades[eleven],x+1)
                    eleven+=1
                    sittingplan.save()
                    c+=1
                    if eleven==elevenGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))  
                elif  x%perDesk==0 and twelve<twelveGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,twelveGrades[twelve],x+1)
                    twelve+=1
                    sittingplan.save()
                    c+=1
                    if twelve==twelveGradesCount:
                        completed+=1
                    print("Başarılı " + str(c))
            elif perDesk==2:
                if  x%perDesk==0 and nine<nineGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,nineGrades[nine],x+1)
                    nine+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))
                elif  x%perDesk==1 and ten<tenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,tenGrades[ten],x+1)
                    ten+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))
                elif x%perDesk==0 and eleven<elevenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,elevenGrades[eleven],x+1)
                    eleven+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))  
                elif x%perDesk==1 and twelve<twelveGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,twelveGrades[twelve],x+1)
                    twelve+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))
            else:
                if   nine<nineGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,nineGrades[nine],x+1)
                    nine+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))
                elif   ten<tenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,tenGrades[ten],x+1)
                    ten+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))
                elif  eleven<elevenGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,elevenGrades[eleven],x+1)
                    eleven+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))  
                elif  twelve<twelveGradesCount:
                    sittingplan = SittingPlan()
                    setSittingPlan(sittingplan,schedule,schoolClass,twelveGrades[twelve],x+1)
                    twelve+=1
                    sittingplan.save()
                    c+=1

                    print("Başarılı " + str(c))



    print("9lar:" + str(nine))
    print("10lar:" + str(ten))
    print("11lar:" + str(eleven))
    print("12lar:" + str(twelve))

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

def class_filter(schedule):
    classes = SchoolClass.objects.filter(school_id=schedule.school_id)
    degree = []
    branch =[]
    for i in classes:
        if (str(i.degree),str(i.degree)) not in degree:
            degree.append((str(i.degree),str(i.degree)))
        if (str(i.branch),str(i.branch)) not in branch:
            branch.append((str(i.branch),str(i.branch)))
    return degree,branch

