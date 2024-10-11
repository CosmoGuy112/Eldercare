# eldercare/urls.py

from django.urls import path
from . import views

app_name = 'eldercare'  # สำคัญมาก! เพื่อให้สามารถเรียกใช้ URL ได้ถูกต้อง

urlpatterns = [
    path('create_appointment/', views.create_appointment, name='create_appointment'),
    path('appointment_list/', views.appointment_list, name='appointment_list'),
    path('caregiver/<int:caregiver_id>/', views.caregiver_profile, name='caregiver_profile'),
    path('elder/<int:elder_id>/', views.elder_profile, name='elder_profile'),
    # ... other URLs for your eldercare app
]