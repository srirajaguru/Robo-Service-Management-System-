from django import forms

from .models import Service, ServiceProgress


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = [
            "customer", "device_type", "brand", "model", "complaint",
            "physical_damage", "priority", "expected_completion_date", "price",
        ]
        widgets = {"expected_completion_date": forms.DateInput(attrs={"type": "date"})}


class StatusForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["status"]


class ProgressForm(forms.ModelForm):
    class Meta:
        model = ServiceProgress
        fields = ["progress_description"]
