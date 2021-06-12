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
from django.urls.conf import re_path
from django.views.static import serve 
from django.contrib import auth
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from exam.views import *
from exam.functions import *
import django



urlpatterns = [
    path('admin/', admin.site.urls),

    #STATIC PATHS
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 

    path('',home,name="index"),

    #AUTHENTICATION PATHS
    path('login/', loginUser),
    path('logout/', logoutUser),
    path('register/', register),

    #PASSWORD RESET PATHS
    path('reset-password/',auth_views.PasswordResetView.
    as_view(template_name="passwordreset.html"),
    name="reset_password"),

    path('reset-password-sent/',auth_views.PasswordResetDoneView.
    as_view(template_name="passwordresetdone.html"),
    name="password_reset_done"),

    path('reset-password/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.
    as_view(template_name="passwordresetform.html"),
    name="password_reset_confirm"),

    path('reset-password-complete/',auth_views.PasswordResetCompleteView.
    as_view(template_name="passwordresetcomplete.html"),
    name="password_reset_complete"),

    #PROFILE EDIT PATH
    path('profile/', profile),

    path('about/', about),

    path('register-school/', registerSchool),

    #SCHOOL ADMIN PATHS
    path('schooladmin/', schooladmin),
    path('schooladmin/upload-student-list/', schooladmin_uploadStudentList),
    path('schooladmin/schedule/', schooladmin_schedule),
    path('schooladmin/schedule/detail/<int:id>', schooladmin_schedule_detail),

    #STUDENT PATHS
    path('student/', student),
    path('student/view-exam-details/', student_viewExamDetails),
    path('student/change-password/', student_changePassword),

    #TEACHER PATHS
    path('teacher/', teacher),
    path('teacher/change-exam-details/', teacher_changeExamDetails),
    path('teacher/view-exam-details/', teacher_viewExamDetails),
    path('teacher/create-exam/', teacher_createExam),

    
    
    path('desk_plan/', desk_plan),
    path('sitting_plan/', sitting_plan),

    path('sql/',cheatingAlgorithm),
    path('mail/',mail_sender_exam)
    


]

# ONLY FOR DEVELOPMENT MODE
if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

