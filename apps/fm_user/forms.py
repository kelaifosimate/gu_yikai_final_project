from django import forms
from .models import UserInfo


class UserForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['uname', 'upwd', 'uemail']

    def clean_uname(self):
        return self.cleaned_data['uname'].strip()

    def clean_uemail(self):
        if self.cleaned_data['uemail']:
            return self.cleaned_data['uemail'].strip()
        return self.cleaned_data['uemail']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserInfo
        fields = ['ushou', 'uaddress', 'uyoubian', 'uphone']

    def clean_ushou(self):
        return self.cleaned_data['ushou'].strip()

    def clean_uaddress(self):
        return self.cleaned_data['uaddress'].strip()