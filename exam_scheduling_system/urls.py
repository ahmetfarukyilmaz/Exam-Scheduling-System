"""exam_scheduling_system URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from os import name
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from exam.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',home,name="index"),
    path('login/', loginUser),
    path('logout/', logoutUser),
    path('register/', register),
    path('profile/', profile),
    path('about', about),
    path('register-school/', registerSchool),
    path('schooladmin/', schooladmin),
    path('schooladmin/upload-student-list/', schooladmin_uploadStudentList),
    path('schooladmin/create-schedule/', schooladmin_createSchedule),
    path('student/', student),
    path('student/view-exam-details/', student_viewExamDetails),
    path('student/change-password/', student_changePassword),
    path('teacher/', teacher),
    path('teacher/change-exam-details/', teacher_changeExamDetails),
    path('teacher/view-exam-details/', teacher_viewExamDetails),
    path('teacher/create-exam/', teacher_createExam),
   
    
    


]

# ONLY FOR DEVELOPMENT MODE
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

