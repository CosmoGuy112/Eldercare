from django import forms
from .models import ElderProfile, CaregiverProfile

class ElderProfileForm(forms.ModelForm):
    class Meta:
        model = ElderProfile
        fields = ['phone_number', 'address', 'medical_conditions', 'imageElder']  # เดา

class CaregiverProfileForm(forms.ModelForm):
    class Meta:
        model = CaregiverProfile
        fields = ['experience', 'imageCaregiver','imageCaregiver']  #เดาๆไว้
