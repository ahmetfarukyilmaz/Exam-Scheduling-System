from exam.models import School,degree_choices,branch_choices
from django import forms
from django.core.exceptions import ValidationError

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
    
    def clean(self):
        degree = self.cleaned_data.get('degree')
        branch = self.cleaned_data.get('branch')
        values ={
            "degree" : degree,
            "branch" : branch,

        }
        return values

    
