from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, EmailField, NullBooleanField
from django.db.models.fields.related import ForeignKey
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class Address(models.Model):

    country=models.CharField(max_length=50)
    city=models.CharField(max_length=50)
    province=models.CharField(max_length=50)
    street=models.CharField(max_length=50)
    postalCode=models.CharField(max_length=20)

    class Meta:
        db_table = 'Address'

    def __str__(self):
        return (self.country+" " + self.city+" " + self.province)


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    schoolNumber = models.PositiveIntegerField()
    email = models.EmailField(null=True,blank=True)
    schoolClass = models.ForeignKey('SchoolClass',on_delete=models.CASCADE,null=True)
    exams = models.ManyToManyField('Exam',blank=True)
    phoneNumber = PhoneNumberField(null=True,blank=True)
    address = models.OneToOneField('Address', on_delete=CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'Student'

    def __str__(self):
        return self.name


class SchoolClass(models.Model):
    degree_choices = [
    ("9", "9"),
    ("10", "10"),
    ("11", "11"),
    ("12", "12"),
    ]

    branch_choices = [
    ("A", "A"),
    ("B", "B"),
    ("C", "C"),
    ("D", "D"),
    ("E", "E"),
    ("F", "F"),
    ("G", "G"),
    ("H", "H"),
    ("I", "I"), 
    ]
    degree = models.CharField(max_length = 20, choices = degree_choices, default = "9")
    branch = models.CharField(max_length = 20, choices = branch_choices, default = "A")
    deskPlan = models.TextField(null=True,blank=True)
    floor = models.IntegerField(null=True,blank=True)
    representative = models.OneToOneField('Student', on_delete = models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'SchoolClass'

    def __str__(self):
        return self.degree + "-" + self.branch   
    

    

class School(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(null=True,blank=True)
    schoolClass=models.ForeignKey('SchoolClass',on_delete=models.CASCADE,null=True,blank=True)
    phoneNumber=PhoneNumberField(null=True,blank=True)
    teacher=models.ForeignKey('Teacher',on_delete=models.CASCADE,null=True,blank=True)
    schoolAdministrator=models.ForeignKey('SchoolAdministrator',on_delete=models.CASCADE,null=True,blank=True)
    address=models.OneToOneField('Address',on_delete=models.CASCADE,null=True,blank=True)
    adminAccessKey = models.CharField('adminAccesssKey',max_length=100, null=True,blank=True,default="abc123123")
    teacherAccessKey = models.CharField('teacherAccessKey', max_length=100, null=True, blank=True, default="abc123")

    class Meta:
        db_table = 'School'
    def __str__(self):
        return self.name




class SchoolAdministrator(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    phoneNumber = PhoneNumberField(null=True,blank=True)
    address = models.OneToOneField('Address', on_delete = models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'SchoolAdministrator'
    def __str__(self):
        return self.name





class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE, primary_key=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(null=True,blank=True)
    phoneNumber = PhoneNumberField(null=True,blank=True)
    address = models.OneToOneField('Address', on_delete = models.CASCADE,null=True,blank=True)

    class Meta:
        db_table = 'Teacher'
    def __str__(self):
        return self.name

class Exam(models.Model):
    name = models.CharField(max_length = 50)
    date = models.DateTimeField()
    duration = models.IntegerField()
    classes = models.ManyToManyField('SchoolClass',related_name='classes')
    examLocation = models.ManyToManyField('SchoolClass',related_name='examLocation')
    observerTeacher = models.OneToOneField('Teacher', on_delete = models.CASCADE,related_name='observer_teacher')
    ownerTeacher = models.OneToOneField('Teacher', on_delete = models.CASCADE,related_name='owner_teacher')
    studentSittingPlan = models.TextField(null=True,blank=True)

    class Meta:
        db_table = 'Exam'

    def __str__(self):
        return str(self.name + " " + self.date)

class Schedule(models.Model):
    name = models.CharField(max_length = 50)
    exams = models.ManyToManyField('Exam')
    administrator = models.OneToOneField('SchoolAdministrator', on_delete = models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

    class Meta:
        db_table = 'Schedule'

    def __str__(self):
        return self.name
    
