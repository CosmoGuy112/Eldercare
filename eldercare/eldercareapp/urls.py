from django.urls import path
from . import views

urlpatterns = [
    path('create_appointment/', views.CreateAppointmentView.as_view(), name='create_appointment'),
    path('appointment_list/', views.AppointmentListView.as_view(), name='appointment_list'),
    path('caregiver/<int:caregiver_id>/', views.CaregiverProfileView.as_view(), name='caregiver_profile'),
    path('elder/<int:elder_id>/', views.ElderProfileView.as_view(), name='elder_profile'),  
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
]
