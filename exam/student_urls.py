from django.conf.urls import url
from .views import *

urlpatterns = {
    url('', student),
    url('view-exam-details/', student_viewExamDetails),
    url('change-password/', student_changePassword),
}