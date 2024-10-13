from django.urls import path 
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),  # หน้าแรก
    path('register/', views.RegisterView.as_view(), name='register'),  # หน้าสมัครสมาชิก
    path('login/', views.LoginView.as_view(), name='login'),  # หน้าล็อกอิน
    path('logout/', views.LogoutView.as_view(), name='logout'),  # หน้าล็อกเอาท์
    path('create_caregiver/', views.UpdateCaregiver.as_view(), name='create_caregiver'),  # หน้าเพิ่มโปรไฟล์ Caregiver
    path('create_elder/', views.UpdateElder.as_view(), name='create_elder'),  # หน้าเพิ่มโปรไฟล์ Elder
    
    path('create_elder_profile/', views.CreateElderProfileView.as_view(), name='create_elder_profile'),  # หน้าเพิ่มโปรไฟล์ Elder
    path('listelder/', views.ListElderView.as_view(), name='listelder'),  # หน้าแสดงรายการ Elder

    # เพิ่ม URL สำหรับ Caregiver Detail และ Booking
    path('caregiver/<int:pk>/', views.CaregiverDetailView.as_view(), name='caregiver_detail'),  # URL สำหรับดูรายละเอียด
    path('caregiver/<int:caregiver_id>/book/', views.BookAppointmentView.as_view(), name='book_appointment'),  # URL สำหรับการจอง
    path('appointment-history/', views.AppointmentHistoryView.as_view(), name='appointment_history'),

]
