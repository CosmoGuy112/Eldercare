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
                # เช็คว่ามี CaregiverProfile และกรอกข้อมูลครบแล้วหรือยัง
                try:
                    caregiver = CaregiverProfile.objects.get(Caregiver=user)
                    # ตรวจสอบว่ากรอกข้อมูลสำคัญครบแล้วหรือยัง
                    if caregiver.name and caregiver.experience_years is not None and caregiver.bio:
                        return redirect('listelder')  # มี profile ครบแล้ว -> ไปหน้า listelder
                    else:
                        return redirect('create_caregiver')  # มี profile แต่ข้อมูลไม่ครบ
                except CaregiverProfile.DoesNotExist:
                    return redirect('create_caregiver')  # ยังไม่มี profile
            else:
                # Elder - เช็คว่ามี ElderProfile และกรอกข้อมูลครบแล้วหรือยัง
                try:
                    elder = ElderProfile.objects.get(elder=user)
                    # ตรวจสอบว่ากรอกข้อมูลสำคัญครบแล้วหรือยัง
                    if elder.name and elder.age is not None and elder.address:
                        return redirect('home')  # มี profile ครบแล้ว -> ไปหน้า home
                    else:
                        return redirect('create_elder')  # มี profile แต่ข้อมูลไม่ครบ
                except ElderProfile.DoesNotExist:
                    return redirect('create_elder')  # ยังไม่มี profile

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
            
            # Save the updated form instance
            form.save()
            return redirect('listelder')  # Redirect to the home page after saving
        
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
            
            # Save the updated form instance
            form.save()
            return redirect('home')  # Redirect to the home page after saving
        
        context = {
            'form': form
        }
        return render(request, 'createelder.html', context)



class ListElderView(LoginRequiredMixin, View):
    def get(self, request):
        # Fetch the caregiver's profile directly linked to the user
        try:
            care_id = request.user.caregiverprofile.id  # Assuming a OneToOneField in your model
        except CaregiverProfile.DoesNotExist:
            return render(request, 'listelder.html', {'error': 'Caregiver profile not found.'})

        # Filter appointments by the caregiver's ID
        applist = Appointment.objects.filter(caregiver_id=care_id)

        # Optionally filter elders related to these appointments
        elder = ElderProfile.objects.filter(id__in=applist.values_list('elder_id', flat=True))

        # Check if the user belongs to the 'Caregiver' group
        is_caregiver = request.user.groups.filter(name='Caregiver').exists()

        # Debugging print statements
        print(applist)
        print(request.user.id)

        # Render the context with elders, appointments, and caregiver status
        context = {
            'elderall': elder,
            'applist': applist,
            'is_caregiver': is_caregiver,
        }
        return render(request, 'listelder.html', context)

    def post(self, request):
        appointment_id = request.POST.get("appointment_id")
        new_status = request.POST.get(f"status_{appointment_id}")

        if appointment_id and new_status:
            try:
                appointment = Appointment.objects.get(id=appointment_id)

                # Verify that the appointment belongs to the current caregiver
                if appointment.caregiver_id != request.user.caregiverprofile.id:
                    return render(request, 'listelder.html', {'error': 'Unauthorized action.'})

                appointment.status = new_status
                appointment.save()

                return redirect('listelder')
            except Appointment.DoesNotExist:
                return render(request, 'listelder.html', {'error': 'Appointment not found.'})

        return redirect('listelder')

    
    
class Elderdetail(View):
    def get(self, request,pk):
        eldernew = ElderProfile.objects.all()
        elder = ElderProfile.objects.filter(id=pk)
        
        
        context = {
            'elderall': elder,
            'eldernew': eldernew
        }
        return render(request, 'elderdetail.html', context)

    

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
        from datetime import datetime
        from django.utils import timezone

        appointment_date = request.POST.get('appointment_date')
        location = request.POST.get('location')

        # ตรวจสอบว่า ElderProfile มีอยู่
        elder_profile = get_object_or_404(ElderProfile, elder=request.user.id)

        # แปลง appointment_date string เป็น datetime object
        try:
            appointment_datetime = datetime.fromisoformat(appointment_date)
            # ทำให้เป็น timezone-aware
            appointment_datetime = timezone.make_aware(appointment_datetime)
        except ValueError:
            messages.error(request, "รูปแบบวันที่ไม่ถูกต้อง")
            return redirect('caregiver_detail', pk=caregiver_id)

        # ตรวจสอบว่าวันที่ที่เลือกไม่ได้อยู่ในอดีต
        if appointment_datetime < timezone.now():
            messages.error(request, "ไม่สามารถจองวันที่ผ่านมาแล้วได้")
            return redirect('caregiver_detail', pk=caregiver_id)

        # ตรวจสอบการจองที่มีอยู่ในวันที่นั้น
        existing_appointment = Appointment.objects.filter(
            caregiver_id=caregiver_id,
            appointment_date=appointment_datetime
        ).exists()

        if existing_appointment:
            messages.error(request, "มีการจองวันและเวลานี้แล้ว กรุณาเลือกวันเวลาอื่น")
            return redirect('caregiver_detail', pk=caregiver_id)

        # ถ้าไม่มีการจองซ้ำ ทำการสร้างการจอง
        Appointment.objects.create(
            elder=elder_profile,
            caregiver_id=caregiver_id,
            appointment_date=appointment_datetime,
            location=location,
            status='scheduled'
        )

        messages.success(request, "จองสำเร็จ!")
        return redirect('appointment_history')  # Redirect ไปหน้าประวัติการจอง
    
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

class MyProfileView(LoginRequiredMixin, View):
    login_url = '/login/'

    def get(self, request):
        # ตรวจสอบว่าเป็น Elder หรือ Caregiver
        is_elder = request.user.groups.filter(name='Elder').exists()
        is_caregiver = request.user.groups.filter(name='Caregiver').exists()

        profile = None
        profile_type = None

        if is_elder:
            try:
                profile = ElderProfile.objects.get(elder=request.user)
                profile_type = 'elder'
            except ElderProfile.DoesNotExist:
                profile = None
        elif is_caregiver:
            try:
                profile = CaregiverProfile.objects.get(Caregiver=request.user)
                profile_type = 'caregiver'
            except CaregiverProfile.DoesNotExist:
                profile = None

        context = {
            'profile': profile,
            'profile_type': profile_type,
            'is_elder': is_elder,
            'is_caregiver': is_caregiver,
        }
        return render(request, 'myprofile.html', context)

class CancelAppointmentView(LoginRequiredMixin, View):
    login_url = '/login/'

    def post(self, request, appointment_id):
        # ดึง appointment
        appointment = get_object_or_404(Appointment, id=appointment_id)

        # ตรวจสอบว่าเป็นเจ้าของ appointment
        if appointment.elder.elder == request.user:
            appointment.status = 'cancelled'
            appointment.save()
            messages.success(request, "ยกเลิกการนัดหมายสำเร็จ")
        else:
            messages.error(request, "คุณไม่มีสิทธิ์ยกเลิกการนัดหมายนี้")

        return redirect('appointment_history')


