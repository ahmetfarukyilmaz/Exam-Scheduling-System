import os
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.template.loader import render_to_string
import pandas as pd


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