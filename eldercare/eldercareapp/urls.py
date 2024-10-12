from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('create_caregiver/', views.UpdateCaregiver.as_view(), name='create_caregiver'),
    path('create_elder/', views.UpdateElder.as_view(), name='create_elder'),
    path('myprofile/', views.MyProfileView.as_view(), name='myprofile'),
    path('create_elder_profile/', views.CreateElderProfileView.as_view(), name='create_elder_profile'),  # เพิ่ม URL สำหรับสร้าง ElderProfile
    path('listelder/', views.listelder.as_view(), name='listelder'),

    # เพิ่ม URL สำหรับ Caregiver Detail และ Booking
    path('caregiver/<int:pk>/', views.CaregiverDetailView.as_view(), name='caregiver_detail'),  # URL สำหรับดูรายละเอียด
    path('caregiver/<int:caregiver_id>/book/', views.BookAppointmentView.as_view(), name='book_appointment'),  # URL สำหรับการจอง
]
