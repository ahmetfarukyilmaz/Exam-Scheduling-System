from django.conf.urls import url
from .views import *

urlpatterns = {
    url('index/', teacher),
    url('change-exam-details/', teacher_changeExamDetails),
    url('view-exam-details/', teacher_viewExamDetails),
}