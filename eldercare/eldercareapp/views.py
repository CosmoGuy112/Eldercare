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
            return redirect('home')
        return render(request, 'login.html', {"form": form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class HomeView(LoginRequiredMixin,ListView):
    login_url = '/login/'
    model = CaregiverProfile
    template_name = 'home.html'
    context_object_name = 'caregivers'  # ตั้งชื่อ context สำหรับเทมเพลต

    def get_queryset(self):
        return CaregiverProfile.objects.all()  # แสดง caregiver ทั้งหมด


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



class listelder(View):
    def get(self,request):
        applist = Appointment.objects.filter(caregiver_id = request.user.id)
        
        context={
            'applist': applist
        }
        return render(request, 'listelder.html', context)
    
    
    
class CaregiverDetailView(DetailView):
    model = CaregiverProfile
    template_name = 'caregiver_detail.html'
    context_object_name = 'caregiver'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['elder_appointments'] = Appointment.objects.all()  # ข้อมูลการนัดหมาย
        return context


class BookAppointmentView(View):
    def post(self, request, caregiver_id):
        appointment_date = request.POST['appointment_date']
        location = request.POST['location']
        caregiver = get_object_or_404(CaregiverProfile, id=caregiver_id)

        # ตรวจสอบว่า ElderProfile มีอยู่
        elder_profile = ElderProfile.objects.filter(elder=request.user).first()
        if not elder_profile:
            # ส่งผู้ใช้ไปยังหน้า Create ElderProfile
            return redirect('create_elder_profile')

        # สร้างการจอง
        appointment = Appointment.objects.create(
            elder=elder_profile,
            caregiver=caregiver,
            appointment_date=appointment_date,
            location=location,
            status='scheduled'
        )
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