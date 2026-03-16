from django.urls import path
from . import views
from .edit import save_fed, edit_fed, delete_fed

from .views import home, get_circles, get_div, get_subdiv, get_stnname, save_bus, edit_bus, delete_bus, save_trf, \
    edit_trf, delete_trf, save_cap, edit_cap, delete_cap

urlpatterns = [
    path('',home.as_view(),name='home'),
    path('get_circles/<str:zone_id>/', get_circles.as_view(), name='get_circles'),
    path('get_div/<str:circle_id>/', get_div.as_view(), name='get_div'),
    path('get_subdiv/<str:div_id>/', get_subdiv.as_view(), name='get_subdiv'),
    path('get_stnname/', get_stnname.as_view(), name='get_stnname'),
    path('save_bus/', save_bus.as_view(), name='save_bus'),
    path('edit_bus/', edit_bus.as_view(), name='edit_bus'),
    path('delete_bus/',delete_bus.as_view(), name='delete_bus'),
    path('save_trf/', save_trf.as_view(), name='save_trf'),
    path('edit_trf/', edit_trf.as_view(), name='edit_trf'),
    path('delete_trf/', delete_trf.as_view(), name='delete_trf'),
    path('save_cap/', save_cap.as_view(), name='save_cap'),
    path('edit_cap/', edit_cap.as_view(), name='edit_cap'),
    path('delete_cap/', delete_cap.as_view(), name='delete_cap'),
    path('save_fed/', save_fed.as_view(), name='save_fed'),
    path('edit_fed/', edit_fed.as_view(), name='edit_fed'),
    path('delete_fed/', delete_fed.as_view(), name='delete_fed'),
]