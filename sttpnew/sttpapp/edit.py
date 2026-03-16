from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView


from .models import owner_master, district_master, zone_master, circle_master, div_master, subdiv_master, \
    substation_master, bus, transformer, capacitorbank, feeder, dgset, stntransformer, bulkloads


class save_fed(View):
    def post(self,request):
        fed_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        voltage = request.POST.get('voltage')
        bus_no = request.POST.get('bus_no')
        bus_name = request.POST.get('bus_name')
        feeder_no = request.POST.get('feeder_no')
        feeder_name = request.POST.get('feeder_name')
        otherend = request.POST.get('otherend')
        connectiontype = request.POST.get('connectiontype')
        cat_loads = request.POST.get('cat_loads')
        autoload_shed = request.POST.get('autoload_shed')
        if fed_id:
            try:
                fed_obj = feeder.objects.get(id=fed_id)
                fed_obj.voltage = voltage
                fed_obj.bus_no = bus_no
                fed_obj.bus_name = bus_name
                fed_obj.feeder_no = feeder_no
                fed_obj.feeder_name = feeder_name
                fed_obj.otherend = otherend
                fed_obj.connectiontype = connectiontype
                fed_obj.cat_loads = cat_loads
                fed_obj.autoload_shed = autoload_shed
                fed_obj.save()
                msg = 'Feeder data updated successfully'
            except feeder.DoesNotExist:
                return JsonResponse({'error': 'Feeder data not found'}, status=404)
        else:
            fed_obj = feeder.objects.create(stn_name=stn_name,voltage=voltage,bus_no=bus_no,bus_name=bus_name,feeder_no=feeder_no,feeder_name=feeder_name,
                                            otherend=otherend,connectiontype=connectiontype,cat_loads=cat_loads,autoload_shed=autoload_shed)
            msg = 'Feeder data saved successfully'
        feederdata = list(feeder.objects.filter(stn_name=stn_name).values())
        return JsonResponse({'msg': msg, 'feederdata': feederdata})

class edit_fed(View):
    def post(self, request):
        fed_id = request.POST.get('id')
        try:
            fed_obj = feeder.objects.get(id=fed_id)
            response_data = {
                'id': fed_obj.id,
                'voltage': fed_obj.voltage,
                'bus_no': fed_obj.bus_no,
                'bus_name': fed_obj.bus_name,
                'feeder_no': fed_obj.feeder_no,
                'feeder_name': fed_obj.feeder_name,
                'otherend': fed_obj.otherend,
                'connectiontype': fed_obj.connectiontype,
                'cat_loads': fed_obj.cat_loads,
                'autoload_shed': fed_obj.autoload_shed
            }
            return JsonResponse(response_data)
        except feeder.DoesNotExist:
            return JsonResponse({'error': 'Feeder data not found'}, status=404)


class delete_fed(View):
    def post(self, request):
        fed_id = request.POST.get('fed_id')
        try:
            fed_obj = feeder.objects.get(id=fed_id)
            fed_obj.delete()
            return JsonResponse({'msg': 'Feeder data deleted successfully'})
        except feeder.DoesNotExist:
            return JsonResponse({'error': 'Feeder data not found'}, status=404)

