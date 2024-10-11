# views.py
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from .models import *
# from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.views import View
# ... (views อื่นๆ)

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Registration successful!")
            return render(request, 'register.html', {"form": form})
            
        # If the form is not valid, render the registration page again with the form and errors
        return render(request, 'register.html', {"form": form})

# @login_required
def create_appointment(request):
    if request.method == 'POST':
        # ... (process form data and create Appointment object)
        return redirect('appointment_list')
    return render(request, 'create_appointment.html')


# @login_required
def appointment_list(request):
    appointments = []  # กำหนดค่าเริ่มต้นให้กับ appointments
    if request.user.is_authenticated:
        if hasattr(request.user, 'elderprofile'):
            appointments = Appointment.objects.filter(elder=request.user.elderprofile)
        elif hasattr(request.user, 'caregiverprofile'):
            appointments = Appointment.objects.filter(caregiver=request.user.caregiverprofile)
        # ถ้าไม่มีทั้งสองกรณี ให้ appointments เป็นลิสต์ว่างหรือแสดงหน้าอื่น ๆ ได้ตามต้องการ

    return render(request, 'appointment_list.html', {'appointments': appointments})

# ... (views อื่นๆ)



def caregiver_profile(request, caregiver_id):
    caregiver = get_object_or_404(CaregiverProfile, pk=caregiver_id)
    return render(request, 'caregiver_profile.html', {'caregiver': caregiver})


def elder_profile(request, elder_id):
    elder = get_object_or_404(ElderProfile, pk=elder_id)
    return render(request, 'elder_profile.html', {'elder': elder})