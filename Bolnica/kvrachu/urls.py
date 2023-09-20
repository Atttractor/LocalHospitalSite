from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('', base, name='home'),
    path('specialitys/', SpecialityListlView.as_view(), name='specialitys'),
    path('specialitys/<str:name>', DoctorHasSpecialityListlView.as_view(), name='doctorHasSpeciality'),
    path('doctors/all', DoctorListlView.as_view(), name='doctors'),
    path('login/', AuthUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', profile, name='profile'),
    path('doctors/(?P<pk>[0-9]+)', DoctorDetailView.as_view(), name='doctor'),
]
