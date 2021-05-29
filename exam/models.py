from django.db import models

# Create your models here.

class School(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    schoolClass=
    phoneNumber=models.CharField(unique=True,max_length=)
    teacher=
    schoolAdministrator=
    address=models.OneToOneField('Address',on_delete=)

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
    
