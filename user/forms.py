from django import forms
from . import models


# class UserForm(forms.Form):
#     account = forms.CharField(max_length=100, required=True)
#     pwd = forms.CharField(max_length=20, min_length=6)

class UserFrom(forms.ModelForm):
    class Meta:
        model = models.User
        fields = "__all__"
