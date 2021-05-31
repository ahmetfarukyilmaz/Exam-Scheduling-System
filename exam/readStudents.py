from django.forms import models
import pandas as pd
from exam.models import Student



studentList = pd.read_excel('../student-list/9a.XLS',header=0,usecols="B,D,I",skiprows=3,na_filter=False,names=["Numara","Ad","Soyad"])

studentClass = Student()
studentClass.user="faruk"
studentClass.name="ahmet"
studentClass.email="ahmet@gmail.com"

studentClass.save()


    