from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class School(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    schoolClass=models.ForeignKey(SchoolClass,on_delete=models.CASCADE)
    phoneNumber=PhoneNumberField()
    teacher=models.ForeignKey(Teacher,on_delete=models.CASCADE)
    schoolAdministrator=models.ForeignKey(SchoolAdministrator,on_delete=models.CASCADE)
    address=models.OneToOneField(Address,on_delete=models.CASCADE)

class SchoolClass(models.Model):


class SchoolAdministrator(models.Model):


class Student(models.Model):

class Teacher(models.Model):


class Address(models.Model):

    country=models.CharField()
    city=models.CharField()
    province=models.CharField()
    street=models.CharField()
    postalCode=models.CharField()


class Exam(models.Model):

class Schedule(models.Model):
    
