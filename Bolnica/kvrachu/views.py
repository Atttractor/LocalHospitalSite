import datetime
from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import generic
from .forms import RegisterUserForm, KartaBolezniForm
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
            patient.doctor_has_patient.add(doctor)
            patient.save()
        else:
            patient = Patient(user_is_patient=user)
            patient.save()
            patient.doctor_has_patient.add(doctor)
            patient.save()

        karta_bolezni = KartaBolezni(patient=patient, bolezn='Пустая карта')
        karta_bolezni.save()

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
        doctor = Doctor.objects.filter(user_is_doctor=self.request.user)

        if patient:
            karta_bolezni = KartaBolezni.objects.filter(patient=self.request.user.patient)
            zapisi_p = Zapis.objects.filter(patient=self.request.user.patient)
            context['zapisi_p'] = zapisi_p
            context['karta_bolezni'] = karta_bolezni
        if doctor:
            zapisi_d = Zapis.objects.filter(doctor=self.request.user.doctor).order_by('date')
            patients = Patient.objects.filter(doctor_has_patient=self.request.user.doctor)
            context['zapisi_d'] = zapisi_d
            context['patietns'] = patients

        return context


class KartaBolezniList(generic.ListView):
    model = KartaBolezni
    template_name = 'kvrachu/karta_bolezni_list.html'

    def get_queryset(self):
        object_list = KartaBolezni.objects.filter(patient=self.kwargs['pk'])
        return object_list

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карты болезни'
        context['patient_pk'] = self.kwargs['pk']
        return context


class KartaBolezniDetail(generic.DetailView):
    model = KartaBolezni
    template_name = 'kvrachu/karta_bolezni_detail.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карта болезни'
        context['form'] = KartaBolezniForm
        return context

    def post(self, request, *args, **kwargs):
        form = KartaBolezniForm(request.POST)
        if form.is_valid():
            bolezn, desription = form.cleaned_data.get('bolezn'), form.cleaned_data.get('desription')
            karta = KartaBolezni.objects.get(pk=kwargs['pk'])
            karta.bolezn = bolezn
            karta.desription = desription
            karta.save()
        return redirect('home')


class KartaBolezniCreate(generic.CreateView):
    form_class = KartaBolezniForm
    template_name = 'kvrachu/karta_bolezni_detail.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление карты'
        context['new_karta_for_patient'] = Patient.objects.get(pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        patient = Patient.objects.get(pk=self.kwargs['pk'])
        bolezn, desription = form.cleaned_data.get('bolezn'), form.cleaned_data.get('desription')
        karta = KartaBolezni(patient=patient, bolezn=bolezn, desription=desription)
        karta.save()
        return redirect('home')


class BoleznInfo(generic.DetailView):
    model = KartaBolezni
    template_name = 'kvrachu/bolezn_info.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Карта болезни'
        return context


def success(request):
    return render(
        request,
        'kvrachu/success.html',
    )
