from django.conf.urls import url
from .views import *

urlpatterns = {
    url('upload-student-list/', schooladmin_uploadStudentList),
    url('create-schedule/', schooladmin_createSchedule),
}
