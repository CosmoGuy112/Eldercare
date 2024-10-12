# Generated by Django 5.1.2 on 2024-10-12 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('eldercareapp', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='caregiverprofile',
            old_name='imageCaregiver',
            new_name='photo',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='date',
        ),
        migrations.RemoveField(
            model_name='appointment',
            name='price',
        ),
        migrations.RemoveField(
            model_name='caregiverprofile',
            name='experience',
        ),
        migrations.RemoveField(
            model_name='caregiverprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='caregiverprofile',
            name='username',
        ),
        migrations.RemoveField(
            model_name='elderprofile',
            name='imageElder',
        ),
        migrations.RemoveField(
            model_name='elderprofile',
            name='medical_conditions',
        ),
        migrations.RemoveField(
            model_name='elderprofile',
            name='phone_number',
        ),
        migrations.RemoveField(
            model_name='elderprofile',
            name='username',
        ),
        migrations.AddField(
            model_name='appointment',
            name='appointment_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caregiverprofile',
            name='bio',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caregiverprofile',
            name='experience_years',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='caregiverprofile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='elderprofile',
            name='age',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='elderprofile',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='elderprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='elder/'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='caregiver',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='eldercareapp.caregiverprofile'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(blank=True, choices=[('scheduled', 'Scheduled'), ('completed', 'Completed'), ('cancelled', 'Cancelled')], max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='elderprofile',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
