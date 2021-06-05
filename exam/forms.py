from exam.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Şifre")
    confirm = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Şifre (Tekrar)")
    school = forms.ModelChoiceField(School.objects.all(), label="Okul")
    accessKey = forms.CharField(max_length=100, label="Erişim Anahtarı")

    def clean(self):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        confirm = self.cleaned_data.get("confirm")
        school = self.cleaned_data.get("school")
        accessKey = self.cleaned_data.get("accessKey")

        if password and confirm and password != confirm:
            raise forms.ValidationError("Şifreler Eşleşmiyor")

        values = {
            "username"  : username,
            "password"  : password,
            "school"    : school,
            "accessKey" : accessKey
        }


        return values

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, label="Kullanıcı Adı")
    password = forms.CharField(max_length=30, widget=forms.PasswordInput, label="Şifre")


class UploadStudentForm(forms.Form):
    degree = forms.ChoiceField(choices=degree_choices)
    branch = forms.ChoiceField(choices = branch_choices)

class TeacherInfoForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ad Soyad")
    email = forms.EmailField(max_length=100, label="Email")
    phoneNumber = PhoneNumberField(label="Telefon")
    country=forms.CharField(max_length=50,label="Ülke")
    city=forms.CharField(max_length=50,label="Şehir")
    province=forms.CharField(max_length=50,label="İlçe")
    street=forms.CharField(max_length=50,label="Sokak")
    postalCode=forms.CharField(max_length=20,label="Posta Kodu")

class SchoolAdminInfoForm(forms.Form):
    name = forms.CharField(max_length=100, label="Ad Soyad")
    email = forms.EmailField(max_length=100, label="Email")
    phoneNumber = PhoneNumberField(label="Telefon")
    country=forms.CharField(max_length=50,label="Ülke")
    city=forms.CharField(max_length=50,label="Şehir")
    province=forms.CharField(max_length=50,label="İlçe")
    street=forms.CharField(max_length=50,label="Sokak")
    postalCode=forms.CharField(max_length=20,label="Posta Kodu")

class StudentInfoForm(forms.Form):
    email = forms.EmailField(max_length=100, label="Email")
    phoneNumber = PhoneNumberField(label="Telefon")
    country=forms.CharField(max_length=50,label="Ülke")
    city=forms.CharField(max_length=50,label="Şehir")
    province=forms.CharField(max_length=50,label="İlçe")
    street=forms.CharField(max_length=50,label="Sokak")
    postalCode=forms.CharField(max_length=20,label="Posta Kodu")

class ExamForm(forms.Form):
    name = forms.CharField(max_length=50, label = "Sınav Adı")
    date = forms.DateTimeField(label = "Sınav Tarihi")
    duration = forms.IntegerField(label = "Sınav Süresi (dakika)")
    classes = forms.ModelMultipleChoiceField(SchoolClass.objects.all(), label = "Sınava girecek sınıflar")
    examLocation = forms.ModelMultipleChoiceField(SchoolClass.objects.all(), label = "Sınav yerleri")
    observerTeacher = forms.ModelMultipleChoiceField(Teacher.objects.all(), label = "Gözetmen Öğretmen")
    ownerTeacher = forms.ModelChoiceField(Teacher.objects.all(), label = "Dersin Öğretmeni")


class registerSchoolForm(forms.Form):
    schoolName = forms.CharField(max_length=100,label="Okul İsmi")
    email=forms.EmailField(label="Email")
    phoneNumber = PhoneNumberField(label="Telefon")
    country=forms.CharField(max_length=50,label="Ülke")
    city=forms.CharField(max_length=50,label="Şehir")
    province=forms.CharField(max_length=50,label="İlçe")
    street=forms.CharField(max_length=50,label="Sokak")
    postalCode=forms.CharField(max_length=20,label="Posta Kodu")
    

    