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


class Patients(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    FIO = models.CharField(max_length=80, help_text='ФИО пациента')
    login = models.CharField(max_length=45, help_text='Логин')
    password = models.CharField(max_length=45, help_text='Пароль')
    doctor_has_patient = models.ManyToManyField('Doctor')
    karta_bolezni_id = models.OneToOneField('KartaBolezni', on_delete=models.PROTECT)

    def __str__(self):
        return self.FIO


class KartaBolezni(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    name = models.CharField(max_length=80, help_text='Название картны болезни')
    bolezn = models.CharField(max_length=45, help_text='Название больницы')

    def __str__(self):
        return self.name


class Doctor(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True, help_text='Уникальный идентификатор')
    FIO = models.CharField(max_length=80, help_text='ФИО доктора')
    speciality_name = models.ForeignKey('Speciality', on_delete=models.PROTECT)
    hospital_id = models.ForeignKey('Hospital', on_delete=models.PROTECT)
    time_table_id = models.ForeignKey('TimeTable', on_delete=models.PROTECT)

    def __str__(self):
        return self.FIO
