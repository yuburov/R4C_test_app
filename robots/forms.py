from django import forms

from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['serial', 'model', 'version', 'created']

    def clean(self):
        cleaned_data = super().clean()
        serial = cleaned_data.get('serial')
        model = cleaned_data.get('model')
        version = cleaned_data.get('version')

        if serial and (not serial.startswith(model) or not serial.endswith(version)):
            raise forms.ValidationError("Serial should start with the model and end with the version")

        return cleaned_data

