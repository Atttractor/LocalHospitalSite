from django.urls import path
from .views import *

urlpatterns = [
    path('', base, name='home'),
    path('specialitys/', SpecialityListlView.as_view(), name='specialitys'),
    path('specialitys/<str:name>', DoctorHasSpecialityListlView.as_view(), name='doctorHasSpeciality'),
    path('doctors/<uuid:pk>', DoctorDetailView.as_view(), name='doctor'),
    path('doctors/all', DoctorListlView.as_view(), name='doctors'),
    path('login/', AuthUser.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('logout/', logout_user, name='logout'),
    path('profile/', UserProfile.as_view(), name='profile'),
    path('bolezn-info/<uuid:pk>', BoleznInfo.as_view(), name='bolezn_info'),
    path('doctors/success', success, name='success'),
    path('add-karta-bolezni/<uuid:pk>', KartaBolezniCreate.as_view(), name='karta_bolezni_add'),
    path('karta-bolezni/<uuid:pk>', KartaBolezniDetail.as_view(), name='karta_bolezni_detail'),
    path('patient-karta-bolezni/<uuid:pk>', KartaBolezniList.as_view(), name='karta_bolezni')
]
