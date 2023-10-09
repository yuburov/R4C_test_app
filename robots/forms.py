from django import forms

from .models import Robot


class RobotForm(forms.ModelForm):
    class Meta:
        model = Robot
        fields = ['model', 'version', 'created']

    def save(self, commit=True):
        # Генерируем серийный номер из модели и версии, разделенных тире
        instance = super(RobotForm, self).save(commit=False)
        instance.serial = f"{self.cleaned_data['model']}-{self.cleaned_data['version']}"

        if commit:
            instance.save()
        return instance

