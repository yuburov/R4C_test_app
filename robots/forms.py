from django import forms
from django.core.validators import validate_email
from .models import Robot


class RobotForm(forms.ModelForm):
    email = forms.CharField(max_length=255, required=True, validators=[validate_email])

    class Meta:
        model = Robot
        fields = ['serial', 'model', 'version', 'created', 'email']

    def clean_serial(self):
        data = self.cleaned_data['serial']
        if not data.startswith(self.cleaned_data['model']):
            raise forms.ValidationError("Serial should start with the model")
        return data