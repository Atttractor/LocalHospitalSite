import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Speciality(models.Model):
    name = models.CharField(max_length=60, primary_key=True, help_text='Название специальности')

    def __str__(self):
        return self.name


class TimeTable(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    name = models.CharField(max_length=20, help_text='Название рсписания')
    monday = models.CharField(max_length=15, help_text='Расписание на пондельник')
    tuesday = models.CharField(max_length=15, help_text='Расписание на вторник')
    wednesday = models.CharField(max_length=15, help_text='Расписание на среду')
    thursday = models.CharField(max_length=15, help_text='Расписание на четверг')
    friday = models.CharField(max_length=15, help_text='Расписание на пятницу')
    saturday = models.CharField(max_length=15, help_text='Расписание на субботу')
    sunday = models.CharField(max_length=15, help_text='Расписание на воскресенье')

    def __str__(self):
        return self.name


class Hospital(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    name = models.CharField(max_length=80, help_text='Название больницы')
    number = models.IntegerField(help_text='Номер больницы')
    time_table_id = models.OneToOneField('TimeTable', on_delete=models.PROTECT)

    def __str__(self):
        return self.name


class Patient(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    user_is_patient = models.OneToOneField(User, on_delete=models.PROTECT, null=False, blank=False)
    doctor_has_patient = models.ManyToManyField('Doctor')

    def __str__(self):
        return self.user_is_patient.first_name + ' ' + self.user_is_patient.last_name


class KartaBolezni(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    bolezn = models.CharField(max_length=45, help_text='Название больницы')
    desription = models.TextField(help_text='Описание болезни')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, help_text='Пациент')

    def __str__(self):
        return self.bolezn


class Doctor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    user_is_doctor = models.OneToOneField(User, on_delete=models.PROTECT, null=False, blank=False)
    speciality_name = models.ForeignKey('Speciality', on_delete=models.PROTECT)
    hospital_id = models.ForeignKey('Hospital', on_delete=models.PROTECT)
    time_table_id = models.ForeignKey('TimeTable', on_delete=models.PROTECT)

    def __str__(self):
        return self.user_is_doctor.first_name + ' ' + self.user_is_doctor.last_name


class Zapis(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    date = models.DateField(help_text='Дата записи')
    doctor = models.ForeignKey(Doctor, on_delete=models.PROTECT, help_text='Пациент')
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, help_text='Пациент')

    def __str__(self):
        return f'Запись на {self.date} к {self.doctor.user_is_doctor.first_name} {self.doctor.user_is_doctor.last_name}'
