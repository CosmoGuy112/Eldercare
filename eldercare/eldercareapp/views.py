from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'register.html', {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            print("Registration successful!")
            return redirect('login')  # redirect to login page after registration
        return render(request, 'register.html', {"form": form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('create_appointment')
        return render(request, 'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class CreateAppointmentView(LoginRequiredMixin, View):
    login_url = 'login'  

    def get(self, request):
        form = AppointmentForm()
        context ={
            'form':form
        }
        return render(request, 'create_appointment.html',context)

    def post(self, request):
        form = AppointmentForm(request.POST)
        if form.is_valid():
            # Save the appointment object to the database
            appointment = form.save(commit=False)
            appointment.user = request.user  # Assign the current user to the appointment
            appointment.save()
            
            # Optionally, add a success message
            print("Appointment created successfully.")
            return redirect('appointment_list')
        else:
            print("fail.")
            # If the form is not valid, render the form again with errors
            context = {
                'form': form
            }
            return render(request, 'create_appointment.html', context)

class AppointmentListView(LoginRequiredMixin, View):
    def get(self, request):
        appointments = Appointment.objects.all()
        # if hasattr(request.user, 'elderprofile'):
        #     appointments = Appointment.objects.filter(elder=request.user.elderprofile)
        # elif hasattr(request.user, 'caregiverprofile'):
        #     appointments = Appointment.objects.filter(caregiver=request.user.caregiverprofile)
        
        
        return render(request, 'appointment_list.html', {'appointments': appointments})

class ElderProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request, elder_id):
        elder = get_object_or_404(ElderProfile, pk=elder_id)
        form = ElderProfileForm(instance=elder) 
        return render(request, 'elder_profile.html', {'elder': elder, 'form': form})

    def post(self, request, elder_id):
        elder = get_object_or_404(ElderProfile, pk=elder_id)
        form = ElderProfileForm(request.POST, request.FILES, instance=elder) 
        if form.is_valid():
            form.save()  
            return redirect('elder_profile', elder.id)  
        return render(request, 'elder_profile.html', {'elder': elder, 'form': form})  
class CaregiverProfileView(LoginRequiredMixin, View):
    login_url = 'login'  

    def get(self, request, caregiver_id):
        caregiver = get_object_or_404(CaregiverProfile, pk=caregiver_id)
        form = CaregiverProfileForm(instance=caregiver)  
        return render(request, 'caregiver_profile.html', {'caregiver': caregiver, 'form': form})

    def post(self, request, caregiver_id):
        caregiver = get_object_or_404(CaregiverProfile, pk=caregiver_id)
        form = CaregiverProfileForm(request.POST, request.FILES, instance=caregiver)  
        if form.is_valid():
            form.save()  
            return redirect('caregiver_profile', caregiver.id) 
        return render(request, 'caregiver_profile.html', {'caregiver': caregiver, 'form': form})  
