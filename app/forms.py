from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django import forms
from django.core.exceptions import ValidationError

from .models import URL


class AddURLForm(forms.ModelForm):
    class Meta:
        model = URL
        fields = ("url",)

    def clean_url(self):
        data = self.cleaned_data["url"]
        if self.instance.user.url_set.filter(url=data).exists():
            raise ValidationError("Duplicate URL.")
        return data

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.add_input(Submit("submit", "Add URL"))
