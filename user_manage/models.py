from django import forms
from django.contrib.auth.models import User


class InfoEditForm(forms.ModelForm):
    is_staff = forms.BooleanField(label="Is Teacher", required=False)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'is_staff')
