from django.contrib.auth import logout, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
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

        date_now = d.date(d.now())
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


def profile(request):
    return render(
        request,
        'kvrachu/user_profile.html'
    )
