import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.db.models import Q
from django.template.loader import render_to_string
import pandas as pd
from exam.models import *
from django.shortcuts import render
import math


def mail_sender(email,teacherAccessKey,adminAccessKey):
    template = render_to_string('email.html',
    {'teacherAccessKey':teacherAccessKey,
    'adminAccessKey':adminAccessKey})
    send_mail('Exam Scheduling System Erişim Anahtarları',
    template,settings.EMAIL_HOST_USER,
    [str(email)],fail_silently=False)

def read_student_list(request):
    uploaded_file = request.FILES['document']
    fs = FileSystemStorage()
    fs.save(uploaded_file.name,uploaded_file)
    base_dir = settings.MEDIA_ROOT
    return pd.read_excel(os.path.join(base_dir,str(uploaded_file.name)),
        header=0,usecols="B,D,I",skiprows=3,na_filter=False,names=["Numara","Ad","Soyad"])


def cheatingAlgorithm(request):
    #will get scheduile id from function parameter
    students= Student.objects.distinct().filter(exams__schedule_id=999)
    schedule = Schedule.objects.get(id=999)
    numberofStudents = students.count()
    #will get school_id from admin's school id
    classes  = SchoolClass.objects.filter(school_id=1)
    numberOfClasses = classes.count()
    print("Öğrenci sayısı:" + str(numberofStudents))
    print("Sınıf sayısı:" + str(numberOfClasses))
    
    nineGrades=students.filter(schoolClass__degree=9).order_by('?')
    nineGradesCount = nineGrades.count()
    tenGrades = students.filter(schoolClass__degree=10).order_by('?')
    tenGradesCount = tenGrades.count()
    elevenGrades = students.filter(schoolClass__degree=11).order_by('?')
    elevenGradesCount = elevenGrades.count()
    twelveGrades = students.filter(schoolClass__degree=12).order_by('?')
    twelveGradesCount=twelveGrades.count()
    maxCount=max(nineGradesCount,tenGradesCount,elevenGradesCount,twelveGradesCount)
    studentPerClass=math.ceil((maxCount*4)/numberOfClasses)
    print("Sınıf başına düşen öğrenci:" + str(studentPerClass))
    print("9. sınıf: " + str(nineGradesCount))
    print("10. sınıf: " + str(tenGradesCount))
    print("11. sınıf: " + str(elevenGradesCount))
    print("12. sınıf: "+  str(twelveGradesCount))
    nine=0
    ten=0
    eleven=0
    twelve=0
    c = 0 ;
    perDesk = 4
    for schoolClass in classes:
        for x in range(40):
            if nine==nineGradesCount or ten==tenGradesCount or eleven==elevenGradesCount or twelve==twelveGradesCount:
                if perDesk==4:
                    perDesk=3
            sittingplan = SittingPlan()
            sittingplan.schedule=schedule
            sittingplan.schoolClass=schoolClass
            if x%perDesk==0 and nine<nineGradesCount:
                sittingplan.student=nineGrades[nine]
                sittingplan.deskNumber=x+1
                nine+=1
                sittingplan.save()
                c+=1
                print("Başarılı " + str(c))
                
            
                
            
            elif x%perDesk==1 and ten<tenGradesCount:
                sittingplan.student=tenGrades[ten]
                sittingplan.deskNumber=x+1
                ten+=1
                sittingplan.save()
                c+=1
                print("Başarılı " + str(c))
                
            
            
            elif x%perDesk==2 and eleven<elevenGradesCount:
                sittingplan.student=elevenGrades[eleven]
                sittingplan.deskNumber=x+1
                eleven+=1
                sittingplan.save()
                c+=1
                print("Başarılı " + str(c))
                
            
            
            elif x%perDesk==3 and twelve<twelveGradesCount:
                sittingplan.student=twelveGrades[twelve]
                sittingplan.deskNumber=x+1
                twelve+=1
                sittingplan.save()
                c+=1
                print("Başarılı " + str(c))
            
            

                
            
            
            
                    
    return render(request,"sql.html",{'data':123})


def handleEmptyQuery(object):
    try:
        return object
    except object.DoesNotExist:
        return False
