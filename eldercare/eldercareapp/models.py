from django.db import models
from django.contrib.auth.models import User


class ElderProfile(models.Model):
    elder = models.OneToOneField(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    photo = models.ImageField(upload_to='elder/', null=True, blank=True)

    def __str__(self):
        return self.name or "Unnamed Elder"


class CaregiverProfile(models.Model):
    Caregiver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True
    )
    name = models.CharField(max_length=100, null=True, blank=True)  # ทำให้ nullable
    experience_years = models.PositiveIntegerField(null=True, blank=True)  # ทำให้ nullable
    bio = models.TextField(null=True, blank=True)  # ทำให้ nullable
    photo = models.ImageField(upload_to='caregiver/', null=True, blank=True)  # ทำให้ nullable  

    def __str__(self):
        return self.name

class Appointment(models.Model):
    elder = models.ForeignKey(ElderProfile, on_delete=models.CASCADE)
    caregiver = models.ForeignKey(CaregiverProfile, on_delete=models.CASCADE, null=True, blank=True)  # ทำให้ nullable
    appointment_date = models.DateTimeField(null=True, blank=True)  # ทำให้ nullable
    location = models.CharField(max_length=255, null=True, blank=True)  # ทำให้ nullable
    status = models.CharField(max_length=20, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], null=True, blank=True)  # ทำให้ nullable

    def __str__(self):
        return f"Appointment for {self.elder.name} with {self.caregiver.name if self.caregiver else 'Unassigned'} on {self.appointment_date}"
