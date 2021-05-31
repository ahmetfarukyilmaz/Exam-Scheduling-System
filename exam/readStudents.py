from django.forms import models
import pandas as pd
from exam.models import Student
from django.conf import settings
import os



def uploadStudents(list):
    base_dir = settings.MEDIA_ROOT
    studentList = pd.read_excel(os.path.join(base_dir,str(list)),header=0,usecols="B,D,I",skiprows=3,na_filter=False,names=["Numara","Ad","Soyad"])
    
    for i in range(len(studentList)):
        if type(studentList.values[i][0])!=int:
            break
        print(str(studentList.values[i][0]) + " " +  studentList.values[i][1] + " " +  studentList.values[i][2])


    