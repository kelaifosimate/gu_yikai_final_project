from django import forms
from .models import OrderInfo, OrderDetailInfo


class OrderForm(forms.ModelForm):
    class Meta:
        model = OrderInfo
        fields = ['user', 'oaddress']

    def clean_oaddress(self):
        return self.cleaned_data['oaddress'].strip()


class OrderDetailForm(forms.ModelForm):
    class Meta:
        model = OrderDetailInfo
        fields = ['goods', 'order', 'count']