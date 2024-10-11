from django.db import models

# Create your models here.
# eldercare/models.py

from django.contrib.auth.models import User


class ElderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # เพิ่มข้อมูลอื่นๆ ของผู้สูงอายุ เช่น เบอร์โทร ที่อยู่ โรคประจำตัว ฯลฯ
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    medical_conditions = models.TextField(blank=True)


class CaregiverProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # เพิ่มข้อมูลอื่นๆ ของผู้ดูแล เช่น ประสบการณ์  ฯลฯ
    experience = models.TextField(blank=True)
    license_number = models.CharField(max_length=50, blank=True)


class Appointment(models.Model):
    elder = models.ForeignKey(ElderProfile, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(CaregiverProfile, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255) # เช่น ชื่อโรงพยาบาล
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], default='pending')


