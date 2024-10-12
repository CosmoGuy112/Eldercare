from django.db import models

class ElderProfile(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)  # ทำให้ nullable
    age = models.PositiveIntegerField(null=True, blank=True)  # ทำให้ nullable
    address = models.CharField(max_length=255, null=True, blank=True)  # ทำให้ nullable
    photo = models.ImageField(upload_to='elder/', null=True, blank=True)  # ทำให้ nullable  

    def __str__(self):
        return self.name

class CaregiverProfile(models.Model):
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
