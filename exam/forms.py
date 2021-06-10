from exam.models import *
from django import forms
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from django.forms import MultipleChoiceField, ChoiceField, Form
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

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
    def __init__(self, class_choices, teacher_choices, *args, **kwargs):
        super(ExamForm, self).__init__(*args, **kwargs)
        self.fields['classes'].choices = class_choices
        self.fields['examLocation'].choices = class_choices
        self.fields['observerTeacher'].choices = teacher_choices



    name = forms.CharField(max_length=50, label = "Sınav Adı")
    date = forms.DateTimeField(label = "Sınav Tarihi")
    duration = forms.IntegerField(label = "Sınav Süresi (dakika)")
    date = forms.DateTimeField(label = "Sınav Tarihi", input_formats = '%Y-%m-%d %H:%M:%S',widget=DateTimePicker(options={
        'sideBySide' : True}))
    duration = forms.IntegerField(label = "Sınav süresi(dakika)")
    classes = forms.MultipleChoiceField(choices=(), widget = forms.CheckboxSelectMultiple, label = "Sınava girecek sınıflar")
    examLocation = forms.MultipleChoiceField(choices=(), widget = forms.CheckboxSelectMultiple,  label = "Sınav yerleri")
    observerTeacher = forms.ChoiceField(choices=(), label = "Gözetmen Öğretmen")


    def clean(self):
        name = self.cleaned_data.get("name")
        date = self.cleaned_data.get("date")
        duration = self.cleaned_data.get("duration")
        classes = self.cleaned_data.get("classes")
        examLocation = self.cleaned_data.get("examLocation")
        observerTeacher = self.cleaned_data.get("observerTeacher")
        ownerTeacher = self.cleaned_data.get("ownerTeacher")


        values = {
            "name"  : name,
            "date"  : date,
            "duration"    : duration,
            "classes" : classes,
            "examLocation": examLocation ,
            "observerTeacher": observerTeacher,
            "ownerTeacher": ownerTeacher,
        }


class registerSchoolForm(forms.Form):
    schoolName = forms.CharField(max_length=100,label="Okul İsmi")
    email=forms.EmailField(label="Email")
    phoneNumber = PhoneNumberField(label="Telefon")
    country=forms.CharField(max_length=50,label="Ülke")
    city=forms.CharField(max_length=50,label="Şehir")
    province=forms.CharField(max_length=50,label="İlçe")
    street=forms.CharField(max_length=50,label="Sokak")
    postalCode=forms.CharField(max_length=20,label="Posta Kodu")


class DeskPlanForm(forms.Form):
    numbers =(
    (0, "Yok"),
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    )
    columns = forms.ChoiceField(choices=numbers, label="Sıra sütunu sayısı", required=True)
    c1 = forms.ChoiceField(choices=numbers, label="Birinci hizadaki sıra sayısı", required=False)
    c2 = forms.ChoiceField(choices=numbers, label="İkinci hizadaki sıra sayısı", required=False)
    c3 = forms.ChoiceField(choices=numbers, label="Üçüncü hizadaki sıra sayısı", required=False)
    c4 = forms.ChoiceField(choices=numbers, label="Dördüncü hizadaki sıra sayısı", required=False)
    c5 = forms.ChoiceField(choices=numbers, label="Beşinci hizadaki sıra sayısı", required=False)
    c6 = forms.ChoiceField(choices=numbers, label="Altıncı hizadaki sıra sayısı", required=False)
    c7 = forms.ChoiceField(choices=numbers, label="Yedinci hizadaki sıra sayısı", required=False)

    def clean(self):
        columns = int(self.cleaned_data.get("columns"))
        c1 = int(self.cleaned_data.get("c1"))
        c2 = int(self.cleaned_data.get("c2")) 
        c3 = int(self.cleaned_data.get("c3")) 
        c4 = int(self.cleaned_data.get("c4")) 
        c5 = int(self.cleaned_data.get("c5")) 
        c6 = int(self.cleaned_data.get("c6")) 
        c7 = int(self.cleaned_data.get("c7"))

        if columns == 0:
            raise forms.ValidationError("Lütfen sütun sayısı girin!")

        if columns == 1:
            print("girdi")
            if c2 + c3 + c4 + c5 + c6 + c7 != 0:
                raise forms.ValidationError("Bir sütun girdiniz. Lütfen sadece birinci sütun için seçim yapın!")
            if c1 == 0:
                raise forms.ValidationError("Bir sütun girdiniz. Lütfen birinci sütun için seçim yapın!")
        if columns == 2:
            if c3 + c4 + c5 + c6 + c7 != 0:
                raise forms.ValidationError("İki sütun girdiniz. Lütfen sadece birinci ve ikinci sütun için seçim yapın!")
            if c1 * c2 == 0:
                raise forms.ValidationError("İki sütun girdiniz. Lütfen birinci ve ikinci sütun için seçim yapın!")
        if columns == 3:
            if c4 + c5 + c6 + c7 != 0:
                raise forms.ValidationError("Üç sütun girdiniz. Lütfen sadece birinci, ikinci ve üçüncü sütun için seçim yapın!")
            if c1 * c2 * c3 == 0:
                raise forms.ValidationError("Üç sütun girdiniz. Lütfen birinci, ikinci ve üçüncü sütun için seçim yapın!")
        if columns == 4:
            if c5 + c6 + c7 != 0:
                raise forms.ValidationError("Dört sütun girdiniz. Lütfen sadece birinci, ikinci, üçüncü ve dördüncü sütun için seçim yapın!")
            if c1 * c2 * c3 * 4 == 0:
                raise forms.ValidationError("Dört sütun girdiniz. Lütfen birinci, ikinci, üçüncü ve dördüncü sütun için seçim yapın!")
        if columns == 5:
            if c6 + c7 != 0:
                raise forms.ValidationError("Beş sütun girdiniz. Lütfen altıncı ve yedinci sütun için seçim yapmayın!")
            if c1 * c2 * c3 * c4 * c5 == 0:
                raise forms.ValidationError("Beş sütun girdiniz. Lütfen birinci, ikinci, üçüncü, dördüncü ve beşinci sütun için seçim yapın!")
        if columns == 6:
            if c7 != 0:
                raise forms.ValidationError("Altı sütun girdiniz. Lütfen yedinci sütun için seçim yapmayın!")
            if c1 * c2 * c3 * c4 * c5 * c6== 0:
                raise forms.ValidationError("Altı sütun girdiniz. Lütfen birinci, ikinci, üçüncü, dördüncü, beşinci ve altıncı sütun için seçim yapın!")
        if columns == 7 and c1 * c2 * c3 * c4 * c5 * c6 * c7 == 0:
            raise forms.ValidationError("Yedi sütun girdiniz. Lütfen tüm sütunlar için seçim yapın!")


        values = {
            "columns"  : columns,
            "c1"  : c1,
            "c2"  : c2,
            "c3"  : c3,
            "c4"  : c4,
            "c5"  : c5,
            "c6"  : c6,
            "c7"  : c7
        }


        return values



class ScheduleForm(forms.Form):
    def __init__(self, examChoices, *args, **kwargs):
        super(ScheduleForm, self).__init__(*args, **kwargs)
        self.fields['exams'].choices = examChoices

    name = forms.CharField(max_length=100,label="Takvim İsmi", required = True)
    exams = forms.MultipleChoiceField(choices=[], label = "Sınavlar", required= True)
    start_date = forms.DateTimeField(label = "Sınav Tarihi", input_formats = '%Y-%m-%d %H:%M:%S',widget=DateTimePicker(options={
        'sideBySide' : True}))
    end_date = forms.DateTimeField(label = "Sınav Tarihi", input_formats = '%Y-%m-%d %H:%M:%S',widget=DateTimePicker(options={
        'sideBySide' : True}))



