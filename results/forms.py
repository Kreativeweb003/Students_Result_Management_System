from django import forms
from .models import Result


class ResultEntryForm(forms.ModelForm):
    class Meta:
        model = Result
        fields = ["ca_score", "exam_score"]
        widgets = {
            "ca_score": forms.NumberInput(attrs={"class": "form-control", "step": "0.5"}),
            "exam_score": forms.NumberInput(attrs={"class": "form-control", "step": "0.5"}),
        }




