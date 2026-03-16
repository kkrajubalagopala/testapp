from django.urls import path

from .dataentry import dataentry, addition, deletion, addlines

from .edit import save_fed, edit_fed, delete_fed, save_dgset, edit_dgset, delete_dgset, save_stntrf, edit_stntrf, \
    delete_stntrf, save_bulk, edit_bulk, delete_bulk, save_reactor, edit_reactor, delete_reactor, get_busnos, \
    save_lines, edit_lines, delete_lines

from .reports import reports, FilterTransformersView, busfilters, stnfilters, recfilters, capfilters, linefilters, \
    fedfilters, dgfilters, stntrffilters, bulkfilters

from .views import home, get_circles, get_div, get_subdiv, get_stnname, save_bus, edit_bus, delete_bus, save_trf, \
    edit_trf, delete_trf, save_cap, edit_cap, delete_cap, auto_stnname, discoms

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
    path('save_dgset/', save_dgset.as_view(), name='save_dgset'),
    path('edit_dgset/', edit_dgset.as_view(), name='edit_dgset'),
    path('delete_dgset/', delete_dgset.as_view(), name='delete_dgset'),
    path('save_stntrf/', save_stntrf.as_view(), name='save_stntrf'),
    path('edit_stntrf/', edit_stntrf.as_view(), name='edit_stntrf'),
    path('delete_stntrf/', delete_stntrf.as_view(), name='delete_stntrf'),
    path('save_bulk/', save_bulk.as_view(), name='save_bulk'),
    path('edit_bulk/', edit_bulk.as_view(), name='edit_bulk'),
    path('delete_bulk/', delete_bulk.as_view(), name='delete_bulk'),
    path('auto_stnname/', auto_stnname.as_view(), name='auto_stnname'),
    path('save_reactor/', save_reactor.as_view(), name='save_reactor'),
    path('edit_reactor/', edit_reactor.as_view(), name='edit_reactor'),
    path('delete_reactor/', delete_reactor.as_view(), name='delete_reactor'),
    path('get_busnos/', get_busnos.as_view(),name='get_busnos'),
    path('save_lines/', save_lines.as_view(), name='save_lines'),
    path('edit_lines/', edit_lines.as_view(), name='edit_lines'),
    path('delete_lines/<int:line_id>/', delete_lines.as_view(), name='delete_lines'),
    path('discoms/',discoms.as_view(),name='discoms'),
    path('reports/',reports.as_view(),name='reports'),
    path('dataentry/',dataentry.as_view(),name='dataentry'),
    path('addition/',addition.as_view(),name='addition'),
    path('deletion/',deletion.as_view(),name='deletion'),
    path('addlines/',addlines.as_view(),name='addlines'),
    #path('filter_transformers/', filter_transformers, name='filter_transformers'),
    path('filter_transformers/', FilterTransformersView.as_view(), name='filter_transformers'),
    path('busfilters/', busfilters.as_view(), name='busfilters'),
    path('stnfilters/', stnfilters.as_view(), name='stnfilters'),
    path('recfilters/', recfilters.as_view(), name='recfilters'),
    path('capfilters/', capfilters.as_view(), name='capfilters'),
    path('linefilters/', linefilters.as_view(), name='linefilters'),
    path('fedfilters/', fedfilters.as_view(), name='fedfilters'),
    path('dgfilters/', dgfilters.as_view(), name='dgfilters'),
    path('stntrffilters/', stntrffilters.as_view(), name='stntrffilters'),
    path('bulkfilters/', bulkfilters.as_view(), name='bulkfilters'),

]