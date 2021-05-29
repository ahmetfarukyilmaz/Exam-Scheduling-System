from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField
from django.db.models.fields.related import ForeignKey
from phonenumber_field.modelfields import PhoneNumberField


degree_choices = (
    ("1", "9"),
    ("2", "10"),
    ("3", "11"),
    ("4", "12"),
)

branch_choices = (
    ("1", "A"),
    ("2", "B"),
    ("3", "C"),
    ("4", "D"),
    ("5", "E"),
    ("6", "F"),
    ("7", "G"),
    ("8", "H"),
    ("9", "I"), 
)

# Create your models here.


class Address(models.Model):

    country=models.CharField()
    city=models.CharField()
    province=models.CharField()
    street=models.CharField()
    postalCode=models.CharField()

class SchoolClass(models.Model):
   degree = models.CharField(max_length = 20, choices = degree_choices, default = "1")
   branch = models.CharField(max_length = 20, choices = branch_choices, default = "1")
   desk_plan = models.TextField()
   floor = models.IntegerField()
   representative = models.OneToOneField(Student, on_delete = models.CASCADE)

class School(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    schoolClass=models.ForeignKey(SchoolClass,on_delete=models.CASCADE)
    phoneNumber=PhoneNumberField()
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    schoolAdministrator=models.ForeignKey(SchoolAdministrator,on_delete=models.CASCADE)
    address=models.OneToOneField(Address,on_delete=models.CASCADE)





class SchoolAdministrator(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = PhoneNumberField()
    address = models.OneToOneField(Address, on_delete = models.CASCADE)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    schoolNumber = models.PositiveIntegerField()
    email = models.EmailField()
    schoolClass = models.ForeignKey(SchoolClass)
    exams = models.ManyToManyField(Exam)
    phoneNumber = PhoneNumberField()
    address = models.OneToOneField(Adress, on_delete=CASCADE)


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phoneNumber = PhoneNumberField()

class Exam(models.Model):
    name = models.CharField(max_length = 50)
    date = models.DateTimeField()
    duration = models.IntegerField()
    classes = models.ManyToManyField(SchoolClass, on_delete = models.CASCADE())
    exam_location = models.ManyToManyField(SchoolClass, on_delete = models.CASCADE())
    observer_teacher = models.OneToOneField(Teacher, on_delete = models.CASCADE())
    owner_teacher = models.OneToOneField(Teacher, on_delete = models.CASCADE())
    student_sitting_plan = models.TextField()

class Schedule(models.Model):
    name = models.CharField(max_length = 50)
    exams = models.ManyToManyField(Exam, on_delete = models.CASCADE())
    administrator = models.OneToOneField(SchoolAdministrator, on_delete = models.CASCADE())
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    
