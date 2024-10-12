from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('caregiver/<int:pk>/', views.CaregiverDetailView.as_view(), name='caregiver_detail'),
    path('book_appointment/<int:caregiver_id>/', views.BookAppointmentView.as_view(), name='book_appointment'),
    path('update_status/<int:appointment_id>/', views.UpdateStatusView.as_view(), name='update_status'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('myprofile/', views.MyProfileView.as_view(), name='myprofile'),
    path('create_profile/', views.CreateElderProfileView.as_view(), name='create_elder_profile'),

]
