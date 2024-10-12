# from django import forms
# from .models import ElderProfile, CaregiverProfile,Appointment

# class ElderProfileForm(forms.ModelForm):
#     class Meta:
#         model = ElderProfile
#         fields = ['id','username','phone_number', 'address', 'medical_conditions', 'imageElder']  # เดา

# class CaregiverProfileForm(forms.ModelForm):
#     class Meta:
#         model = CaregiverProfile
#         fields = ['id','username','experience', 'phone_number','imageCaregiver']  #เดาๆไว้

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
        
