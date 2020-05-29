from django import forms
from . import models


class ResourceModelForm(forms.ModelForm):
    class Meta:
        model = models.Resource
        fields = "__all__"
