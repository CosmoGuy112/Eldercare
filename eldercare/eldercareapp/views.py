from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from .models import *
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from django.views.generic import ListView, DetailView


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
    
    
class HomeView(ListView):
    model = CaregiverProfile
    template_name = 'home.html'

class CaregiverDetailView(DetailView):
    model = CaregiverProfile
    template_name = 'caregiver_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Assuming you have a way to get the elder user
        context['elder_appointments'] = Appointment.objects.filter(elder=self.request.user.elderprofile)
        return context

class BookAppointmentView(View):
    def post(self, request, caregiver_id):
        appointment_date = request.POST['appointment_date']
        caregiver = get_object_or_404(CaregiverProfile, id=caregiver_id)
        # Create appointment here, assuming you have the elder information
        Appointment.objects.create(
            elder=request.user.elderprofile,
            caregiver=caregiver,
            appointment_date=appointment_date,
            location='Hospital Phyathai',  # replace with actual location if needed
            status='scheduled'
        )
        return redirect('caregiver_detail', pk=caregiver_id)

class UpdateStatusView(View):
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = request.POST['status']
        appointment.save()
        return redirect('caregiver_detail', pk=appointment.caregiver.id)