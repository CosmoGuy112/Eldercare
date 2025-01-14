from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        ('Elder', 'Elder'),
        ('Caregiver', 'Caregiver'),
    )
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True, label="User Type")

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')


class ElderProfileForm(forms.ModelForm):
    class Meta:
        model = ElderProfile
        fields = ['id','name','age', 'address', 'photo', 'contact']  # เดา

class CaregiverProfileForm(forms.ModelForm):
    class Meta:
        model = CaregiverProfile
        fields = ['id','name','experience_years', 'bio','photo']  
        
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['bio'].widget = forms.Textarea(attrs={'rows': 4, 'placeholder': 'Write a brief bio...'})
    #     self.fields['photo'].required = False  # Make the photo optional if you want

# class AppointmentForm(forms.ModelForm):
#     class Meta:
        
#         model = Appointment
#         fields = ['elder', 'caregiver', 'date', 'location', 'price', 'status'] 
#         widgets = {
#             'date': forms.DateInput(attrs={'type': 'date'}),  
#             'location': forms.TextInput(attrs={'placeholder': 'Enter location (e.g., hospital name)'}),
#             'price': forms.NumberInput(attrs={'placeholder': 'Enter price'}),
#             'status': forms.Select(),  
#         }
        
