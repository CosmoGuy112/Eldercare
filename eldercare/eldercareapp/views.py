from typing import Any
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404,HttpResponse
from .models import *
from django.shortcuts import get_object_or_404
from django.views import View
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from .forms import *
from django.views.generic import ListView, DetailView,CreateView
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse_lazy
from django.contrib import messages  
from django.utils import timezone 
from django.http import HttpResponseRedirect

class RegisterView(View):
    def get(self, request):
        form = RegisterForm()  
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)  
        if form.is_valid():
            user = form.save()

            user_type = form.cleaned_data.get('user_type')
            try:
                if user_type == 'Elder':
                    group = Group.objects.get(name="Elder")
                else:
                    group = Group.objects.get(name="Caregiver")
                group.user_set.add(user)
            except Group.DoesNotExist:
                form.add_error(None, "Group does not exist.")
                return render(request, 'register.html', {'form': form})

            login(request, user)
            return redirect('login')  
        return render(request, 'register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login.html', {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # ตรวจสอบกลุ่มของผู้ใช้
            if user.groups.filter(name='Caregiver').exists():
                return redirect('listelder')  # ถ้าเป็น Caregiver ไปหน้า listelder
            else:
                return redirect('home')  # ถ้าเป็น Elder ไปหน้า home
        
        return render(request, 'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    model = CaregiverProfile
    template_name = 'home.html'
    context_object_name = 'caregivers'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_caregiver'] = self.request.user.groups.filter(name='Caregiver').exists()
        return context

class UpdateCaregiver(View):
    def get(self, request):
        # Get the caregiver profile for the logged-in user or create a new one
        caregiver_profile, created = CaregiverProfile.objects.get_or_create(Caregiver=request.user)

        # Instantiate the form with the existing caregiver data
        form = CaregiverProfileForm(instance=caregiver_profile)

        # Create the context with the form
        context = {
            'form': form
        }

        return render(request, 'createcaregiver.html', context)
    

    def post(self, request):
        # Get the caregiver profile for the logged-in user or return a 404 if not found
        caregiver_profile, created = CaregiverProfile.objects.get_or_create(Caregiver=request.user)

        # Handle the form submission
        form = CaregiverProfileForm(request.POST, request.FILES, instance=caregiver_profile)

        if form.is_valid():
            print("Form is valid.")
            # Save the updated form instance
            form.save()
            return redirect('home')  # Redirect to the home page after saving
        
        context = {
            'form': form
        }
        return render(request, 'createcaregiver.html', context)
    
    
    
class UpdateElder(View):
    def get(self, request):
        # Get the elder profile for the logged-in user or create a new one
        elder_profile, created = ElderProfile.objects.get_or_create(elder=request.user)

        # Instantiate the form with the existing elder data
        form = ElderProfileForm(instance=elder_profile)

        # Create the context with the form
        context = {
            'form': form
        }

        return render(request, 'createelder.html', context)
    

    def post(self, request):
        # Get the elder profile for the logged-in user or return a 404 if not found
        elder_profile, created = ElderProfile.objects.get_or_create(elder=request.user)

        # Handle the form submission
        form = ElderProfileForm(request.POST, request.FILES, instance=elder_profile)

        if form.is_valid():
            print("Form is valid.")
            # Save the updated form instance
            form.save()
            return redirect('home')  # Redirect to the home page after saving
        
        context = {
            'form': form
        }
        return render(request, 'createelder.html', context)



class ListElderView(LoginRequiredMixin, View):
    def get(self, request):
        applist = Appointment.objects.filter(caregiver_id=request.user.id)
        is_caregiver = request.user.groups.filter(name='Caregiver').exists()
        
        context = {
            'applist': applist,
            'is_caregiver': is_caregiver,
        }
        return render(request, 'listelder.html', context)

    def post(self, request):
        appointment_id = request.POST.get("appointment_id")
        new_status = request.POST.get(f"status_{appointment_id}")
        
        if appointment_id and new_status:
            try:
                # Update the appointment status in the database
                appointment = Appointment.objects.get(id=appointment_id)
                appointment.status = new_status
                appointment.save()

                # Redirect back to the appointment list view
                return redirect('listelder')
            except Appointment.DoesNotExist:
                # Handle the case where the appointment doesn't exist
                return render(request, 'listelder.html', {'error': 'Appointment not found.'})
        
        return redirect('listelder')  # Default fallback to the list page
    
    
class CaregiverDetailView(DetailView):
    model = CaregiverProfile
    template_name = 'caregiver_detail.html'
    context_object_name = 'caregiver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['elder_appointments'] = Appointment.objects.all()  # ข้อมูลการนัดหมาย
        return context



class BookAppointmentView(LoginRequiredMixin, View):
    def post(self, request, caregiver_id):
        appointment_date = request.POST.get('appointment_date')
        location = request.POST.get('location')

        # ตรวจสอบว่า ElderProfile มีอยู่
        elder_profile = get_object_or_404(ElderProfile, elder=request.user)

        # ตรวจสอบการจองที่มีอยู่ในวันที่นั้น
        existing_appointment = Appointment.objects.filter(
            caregiver_id=caregiver_id,
            appointment_date=appointment_date
        ).exists()

        if existing_appointment:
            messages.error(request, "มีการจองวันซ้ำกันในวันนี้")  
            return redirect('caregiver_detail', pk=caregiver_id)  # Redirect กลับไปที่หน้า detail

        # ถ้าไม่มีการจองซ้ำ ทำการสร้างการจอง
        Appointment.objects.create(
            elder=elder_profile,
            caregiver_id=caregiver_id,
            appointment_date=appointment_date,
            location=location,
            status='scheduled'
        )

        messages.success(request, "จองสำเร็จ!")  # Alert สีเขียว
        return redirect('caregiver_detail', pk=caregiver_id)
    
class UpdateStatusView(View):
    def post(self, request, appointment_id):
        appointment = get_object_or_404(Appointment, id=appointment_id)
        appointment.status = request.POST['status']
        appointment.save()
        return redirect('caregiver_detail', pk=appointment.caregiver.id)

class CreateElderProfileView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = ElderProfile
    form_class = ElderProfileForm
    template_name = 'create_elder_profile.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        form.instance.elder = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.request.user.groups.filter(name='Elder').exists()

class MyProfileView(LoginRequiredMixin, View):
    login_url = '/auth/login/'

    def get(self, request):
        try:
            profile = ElderProfile.objects.get(elder=request.user)
            form = ElderProfileForm(instance=profile)
        except ObjectDoesNotExist:
            return HttpResponse("<h1>ไม่พบโปรไฟล์ของคุณ</h1>")
        return render(request, "myprofile.html", {'form': form})

    def post(self, request):
        profile = get_object_or_404(ElderProfile, elder=request.user)
        form = ElderProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('home')
        return render(request, "myprofile.html", {"form": form})
    

class AppointmentHistoryView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # ดึงข้อมูล ElderProfile ของผู้ใช้ที่เข้าสู่ระบบ
        elder_profile = get_object_or_404(ElderProfile, elder=request.user)
        
        # ดึงข้อมูลการนัดหมายที่เกี่ยวข้องกับ ElderProfile นี้
        appointments = Appointment.objects.filter(elder=elder_profile)

        context = {
            'appointments': appointments
        }
        return render(request, 'appointment_history.html', context)

    
