from django.db import models

# Create your models here.
# eldercare/models.py

from django.contrib.auth.models import User


class ElderProfile(models.Model):
    username = models.CharField(max_length=150)
    # เพิ่มข้อมูลอื่นๆ ของผู้สูงอายุ เช่น เบอร์โทร ที่อยู่ โรคประจำตัว ฯลฯ
    phone_number = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    medical_conditions = models.TextField(blank=True)
    imageElder = models.ImageField(upload_to='Elder/', null=True, blank=True)
    def __str__(self):
        return self.username


class CaregiverProfile(models.Model):
    username = models.CharField(max_length=150)
    experience = models.TextField(blank=True)
    phone_number = models.CharField(max_length=20, blank=True)  # เพิ่มฟิลด์นี้
    imageCaregiver = models.ImageField(upload_to='caregiver/', null=True, blank=True)
    
    def __str__(self):
        return self.username

class Appointment(models.Model):
    elder = models.ForeignKey(ElderProfile, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(CaregiverProfile, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateField()
    location = models.CharField(max_length=255)  # เช่น ชื่อโรงพยาบาล
    price = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(
        max_length=20, 
        choices=[
            ('scheduled', 'Scheduled'),           # นัดหมายที่กำหนดไว้
            ('in_transit', 'In Transit'),         # กำลังเดินทาง
            ('completed', 'Completed'),            # เสร็จสิ้น
            ('cancelled', 'Cancelled')             # ยกเลิก
        ], 
        default='scheduled'
    )
    def __str__(self):
        return f'Appointment with {self.elder.username} for {self.caregiver.username} on {self.date.strftime("YYYY-MM-DD HH:mm")}'
