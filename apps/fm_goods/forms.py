from django import forms
from .models import GoodsInfo


class GoodsForm(forms.ModelForm):
    class Meta:
        model = GoodsInfo
        fields = ['gtitle', 'gpic', 'gprice', 'gjianjie', 'gkucun', 'gcontent']

    def clean_gtitle(self):
        return self.cleaned_data['gtitle'].strip()

    def clean_gjianjie(self):
        return self.cleaned_data['gjianjie'].strip()

    def clean_gcontent(self):
        return self.cleaned_data['gcontent'].strip()