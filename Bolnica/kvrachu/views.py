import datetime

from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterUserForm
from .models import *
from datetime import datetime as d
from datetime import timedelta


def base(request):
    return render(
        request,
        'base.html',
    )


class DoctorListlView(generic.ListView):
    model = Doctor
    template_name = 'doctor_list.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все специалисты'

        return context


class DoctorDetailView(generic.DetailView):
    model = Doctor
    template_name = 'kvrachu/doctor_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        date_now = d.date(d.now() + timedelta(1))
        days_of_week = ['Понедельник',
                        'Вторник',
                        'Среда',
                        'Четверг',
                        'Пятница',
                        'Суббота',
                        'Воскресенье']
        days = []
        period = 7
        for i in range(period):
            day_of_week = i % 7
            days.append((days_of_week[d.weekday(date_now + timedelta(day_of_week))], date_now + timedelta(i)))

        f = TimeTable.objects.get(doctor=context['object'])

        context['dates'] = days
        context['time_table'] = f

        return context

    def post(self, request, *args, **kwargs):
        user = request.user
        day = list(dict(request.POST).keys())[-1]
        date = datetime.datetime.strptime(day, '%d.%m.%Y').date()
        doctor = Doctor.objects.get(pk=kwargs['pk'])

        patient = Patient.objects.filter(user_is_patient=user)
        if patient:
            patient = user.patient
        else:
            patient = Patient(user_is_patient=user)
            Patient.doctor_has_patient = doctor
            patient.save()

        zapis = Zapis.objects.get_or_create(patient=patient,
                                            doctor=doctor,
                                            date=date)

        message = 'Вы успешно записались к врачу'
        if not zapis[1]:
            message = 'Ты уже записан к этому врачу на этот день'
        output = "\033[31m{}\033[0m".format(f'{message}')
        print(output)

        return HttpResponseRedirect('success')


class DoctorHasSpecialityListlView(generic.ListView):
    model = Doctor
    template_name = 'doctor_list.html'

    def get_queryset(self):
        object_list = Doctor.objects.filter(speciality_name=self.kwargs['name'])
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'{self.kwargs["name"]}'

        return context


class SpecialityListlView(generic.ListView):
    model = Speciality
    template_name = 'speciality_list.html'


class RegisterUser(generic.CreateView):
    form_class = RegisterUserForm
    template_name = 'kvrachu/register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class AuthUser(LoginView):
    form_class = AuthenticationForm
    template_name = 'kvrachu/login.html'

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


class UserProfile(generic.TemplateView):
    template_name = 'kvrachu/user_profile.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Личный кабинет'
        patient = Patient.objects.filter(user_is_patient=self.request.user)

        if patient:
            output = "\033[31m{}\033[0m".format(f'{self.request.user.patient}')
            print(output)
            karta_bolezni = KartaBolezni.objects.filter(patient=self.request.user.patient)
            zapisi = Zapis.objects.filter(patient=self.request.user.patient)
            context['zapisi'] = zapisi
            context['karta_bolezni'] = karta_bolezni

        return context


def test(request):
    if request.method == 'POST':
        print('post')

    return render(
        request,
        'kvrachu/test.html',
    )


def success(request):
    return render(
        request,
        'kvrachu/success.html',
    )
