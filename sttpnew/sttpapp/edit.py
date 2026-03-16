from django.core.serializers import json
from django.http import JsonResponse, request
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView


from .models import owner_master, district_master, zone_master, circle_master, div_master, subdiv_master, \
    substation_master, bus, transformer, capacitorbank, feeder, dgset, stntransformer, bulkloads, lines, reactor
from .views import get_stnname


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
        fedcmsndt = request.POST.get('fedcmsndt')
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
                fed_obj.fedcmsndt = fedcmsndt
                fed_obj.save()
                msg = 'Feeder data updated successfully'
            except feeder.DoesNotExist:
                return JsonResponse({'error': 'Feeder data not found'}, status=404)
        else:
            fed_obj = feeder.objects.create(stn_name=stn_name,voltage=voltage,bus_no=bus_no,bus_name=bus_name,feeder_no=feeder_no,feeder_name=feeder_name,
                                            otherend=otherend,connectiontype=connectiontype,cat_loads=cat_loads,autoload_shed=autoload_shed,fedcmsndt=fedcmsndt)
            msg = 'Feeder data saved successfully'
        feederdata = list(feeder.objects.filter(stn_name=stn_name,deleted=False).values())
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
                'autoload_shed': fed_obj.autoload_shed,
                'fedcmsndt': fed_obj.fedcmsndt,
            }
            return JsonResponse(response_data)
        except feeder.DoesNotExist:
            return JsonResponse({'error': 'Feeder data not found'}, status=404)


class delete_fed(View):
    def post(self, request):
        fed_id = request.POST.get('fed_id')
        try:
            fed_obj = feeder.objects.get(id=fed_id)
            fed_obj.deleted = True
            fed_obj.save()
            return JsonResponse({'msg': 'Feeder data deleted successfully'})
        except feeder.DoesNotExist:
            return JsonResponse({'error': 'Feeder data not found'}, status=404)


class save_dgset(View):
    def post(self, request):
        dg_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        dgset_id = request.POST.get('dgset_id')
        availability = request.POST.get('availability')
        rating = request.POST.get('rating')
        dgcmsndt = request.POST.get('dgcmsndt')

        if dg_id:
            try:
                dgset_obj = dgset.objects.get(id=dg_id)
                dgset_obj.stn_name = stn_name
                dgset_obj.dgset_id = dgset_id
                dgset_obj.availability = availability
                dgset_obj.rating = rating
                dgset_obj.dgcmsndt = dgcmsndt
                dgset_obj.save()
                msg = 'DGSET details updated successfully'
            except dgset.DoesNotExist:
                return JsonResponse({'error': 'DGSET not found'}, status=404)
        else:  # Otherwise, create a new record
            dgset_obj = dgset.objects.create(stn_name=stn_name,dgset_id=dgset_id,availability=availability,rating=rating,dgcmsndt=dgcmsndt)
            msg = 'DGSET details saved successfully'
        dgsetdata = list(dgset.objects.filter(stn_name=stn_name,deleted=False).values())  # Convert queryset to list of dictionaries
        return JsonResponse({'msg': msg, 'dgsetdata': dgsetdata})

class edit_dgset(View):
    def post(self, request):
        dg_id = request.POST.get('dg_id')
        try:
            dgset_obj = dgset.objects.get(id=dg_id)
            response_data = {
                'id': dgset_obj.id,
                'dgset_id': dgset_obj.dgset_id,
                'availability': dgset_obj.availability,
                'rating': dgset_obj.rating,
                'dgcmsndt': dgset_obj.dgcmsndt,

            }
            return JsonResponse(response_data)
        except dgset.DoesNotExist:
            return JsonResponse({'error': 'DGSET not found'}, status=404)

class delete_dgset(View):
    def post(self, request):
        dg_id = request.POST.get('dg_id')
        try:
            dgset_obj = dgset.objects.get(id=dg_id)
            dgset_obj.deleted = True
            dgset_obj.save()
            return JsonResponse({'msg': 'DGSET deleted successfully'})
        except dgset.DoesNotExist:
            return JsonResponse({'error': 'DGSET not found'}, status=404)


class save_stntrf(View):
    def post(self,request):
        stf_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        prim_volt = request.POST.get('prim_volt')
        sec_volt = request.POST.get('sec_volt')
        rating = request.POST.get('rating')
        stntrf_id = request.POST.get('stntrf_id')
        source = request.POST.get('source')
        trnf_id = request.POST.get('trnf_id')
        ict_capacity = request.POST.get('ict_capacity')
        feeder_name = request.POST.get('feeder_name')
        discomss = request.POST.get('discomss')
        length_feeder = request.POST.get('length_feeder')
        feed_type = request.POST.get('feed_type')
        bus_id = request.POST.get('bus_id')
        trftype = request.POST.get('trftype')
        stntfcmsndt = request.POST.get('stntfcmsndt')
        if stf_id:
            try:
                stntrf_obj = stntransformer.objects.get(id=stf_id)
                stntrf_obj.prim_volt = prim_volt
                stntrf_obj.sec_volt = sec_volt
                stntrf_obj.rating = rating
                stntrf_obj.stntrf_id = stntrf_id
                stntrf_obj.source = source
                stntrf_obj.trnf_id = trnf_id
                stntrf_obj.ict_capacity = ict_capacity
                stntrf_obj.feeder_name = feeder_name
                stntrf_obj.discomss = discomss
                stntrf_obj.length_feeder = length_feeder
                stntrf_obj.feed_type = feed_type

                stntrf_obj.bus_id = bus_id
                stntrf_obj.trftype = trftype
                stntrf_obj.stntfcmsndt = stntfcmsndt

                stntrf_obj.save()
                msg = 'Station Transformer data updated successfully'
            except stntransformer.DoesNotExist:
                return JsonResponse({'error': 'Station Transformer data not found'}, status=404)
        else:
            stntrf_obj = stntransformer.objects.create(stn_name=stn_name, prim_volt=prim_volt, sec_volt=sec_volt,
                                                       rating=rating, stntrf_id=stntrf_id, source=source,
                                                       trnf_id=trnf_id, ict_capacity=ict_capacity,
                                                       feeder_name=feeder_name, discomss=discomss,
                                                       length_feeder=length_feeder,
                                                       feed_type=feed_type,  bus_id=bus_id,
                                                       trftype=trftype,stntfcmsndt=stntfcmsndt)
            msg = 'Station Transformer data saved successfully'
        stntrfdata = list(stntransformer.objects.filter(stn_name=stn_name,deleted=False).values())
        return JsonResponse({'msg': msg, 'stntrfdata': stntrfdata})

class edit_stntrf(View):
    def post(self, request):
        stf_id = request.POST.get('id')
        try:
            stntrf_obj = stntransformer.objects.get(id=stf_id)
            response_data = {
                'id': stntrf_obj.id,
                'prim_volt': stntrf_obj.prim_volt,
                'sec_volt': stntrf_obj.sec_volt,
                'rating': stntrf_obj.rating,
                'stntrf_id': stntrf_obj.stntrf_id,
                'source': stntrf_obj.source,
                'trnf_id': stntrf_obj.trnf_id,
                'ict_capacity': stntrf_obj.ict_capacity,
                'feeder_name': stntrf_obj.feeder_name,
                'discomss': stntrf_obj.discomss,
                'length_feeder': stntrf_obj.length_feeder,
                'feed_type': stntrf_obj.feed_type,
                'bus_id' : stntrf_obj.bus_id,
                'trftype' : stntrf_obj.trftype,
                'stntfcmsndt' : stntrf_obj.stntfcmsndt,
            }

            return JsonResponse(response_data)
        except stntransformer.DoesNotExist:
            return JsonResponse({'error': 'Station Transformer data not found'}, status=404)


class delete_stntrf(View):
    def post(self, request):
        stf_id = request.POST.get('stf_id')
        try:
            stntrf_obj = stntransformer.objects.get(id=stf_id)
            stntrf_obj.deleted = True
            stntrf_obj.save()
            return JsonResponse({'msg': 'Station Transformer data deleted successfully'})
        except stntransformer.DoesNotExist:
            return JsonResponse({'error': 'Station Transformer data not found'}, status=404)

class save_bulk(View):
    def post(self, request):
        bulk_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        bus_volt = request.POST.get('bus_volt')
        bus_no = request.POST.get('bus_no')
        bus_name = request.POST.get('bus_name')
        cons_name = request.POST.get('cons_name')
        cons_cat = request.POST.get('cons_cat')
        discom = request.POST.get('discom')
        contr_load = request.POST.get('contr_load')
        bulkcmsndt = request.POST.get('bulkcmsndt')

        if bulk_id:
            try:
                bulk_obj = bulkloads.objects.get(id=bulk_id)
                bulk_obj.stn_name = stn_name
                bulk_obj.bus_volt = bus_volt
                bulk_obj.bus_no = bus_no
                bulk_obj.bus_name = bus_name
                bulk_obj.cons_name = cons_name
                bulk_obj.cons_cat = cons_cat
                bulk_obj.discom = discom
                bulk_obj.contr_load = contr_load
                bulk_obj.bulkcmsndt = bulkcmsndt
                bulk_obj.save()
                msg = 'Bulk Load details updated successfully'
            except bulkloads.DoesNotExist:
                return JsonResponse({'error': 'Bulk Load data not found'}, status=404)
        else:  # Otherwise, create a new record
            bulk_obj = bulkloads.objects.create(stn_name=stn_name,bus_volt=bus_volt,bus_no=bus_no,bus_name=bus_name,cons_name=cons_name,
                                                     cons_cat=cons_cat,discom=discom,contr_load=contr_load,bulkcmsndt=bulkcmsndt)
            msg = 'Bulk Load details saved successfully'
        bulkloadsdata = list(bulkloads.objects.filter(stn_name=stn_name,deleted=False).values())  # Convert queryset to list of dictionaries
        return JsonResponse({'msg': msg, 'bulkloadsdata': bulkloadsdata})


class edit_bulk(View):
    def post(self, request):
        bulk_id = request.POST.get('bulk_id')
        try:
            bulk_obj = bulkloads.objects.get(id=bulk_id)
            response_data = {
                'id': bulk_obj.id,
                'bus_volt': bulk_obj.bus_volt,
                'bus_no': bulk_obj.bus_no,
                'bus_name': bulk_obj.bus_name,
                'cons_name': bulk_obj.cons_name,
                'cons_cat': bulk_obj.cons_cat,
                'discom': bulk_obj.discom,
                'contr_load': bulk_obj.contr_load,
                'bulkcmsndt': bulk_obj.bulkcmsndt,
            }
            return JsonResponse(response_data)
        except bulkloads.DoesNotExist:
            return JsonResponse({'error': 'Bulk Load data not found'}, status=404)

class delete_bulk(View):
    def post(self, request):
        bulk_id = request.POST.get('bulk_id')
        try:
            bulk_obj = bulkloads.objects.get(id=bulk_id)
            bulk_obj.deleted = True
            bulk_obj.save()
            return JsonResponse({'msg': 'Bulk Load data deleted successfully'})
        except bulkloads.DoesNotExist:
            return JsonResponse({'error': 'Bulk Load data not found'}, status=404)



class save_reactor(View):
    def post(self,request):
        reactor_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        react_type = request.POST.get('react_type')
        react_voltage = request.POST.get('react_voltage')
        react_bus = request.POST.get('react_bus')
        react_busname = request.POST.get('react_busname')
        line_id = request.POST.get('line_id')
        line_name = request.POST.get('line_name')
        react_cap = request.POST.get('react_cap')
        react_id = request.POST.get('react_id')
        convertible = request.POST.get('convertible')
        rated_voltage = request.POST.get('rated_voltage')
        reccmsndt = request.POST.get('reccmsndt')

        if reactor_id:
            try:
                reactor_obj = reactor.objects.get(id=reactor_id)
                reactor_obj.stn_name = stn_name
                reactor_obj.react_type = react_type
                reactor_obj.react_voltage = react_voltage
                reactor_obj.react_bus = react_bus
                reactor_obj.react_busname = react_busname
                reactor_obj.line_id = line_id
                reactor_obj.line_name = line_name
                reactor_obj.react_cap = react_cap
                reactor_obj.react_id = react_id
                reactor_obj.convertible = convertible
                reactor_obj.rated_voltage = rated_voltage
                reactor_obj.reccmsndt = reccmsndt
                reactor_obj.save()
                msg = 'Reactor details Updated successfully'
            except reactor.DoesNotExist:
                return JsonResponse({'error': 'Reactor data not found'}, status=404)
        else:
            reactor_obj = reactor.objects.create(stn_name=stn_name,react_type=react_type,react_voltage=react_voltage,react_bus=react_bus,
                                                 react_busname=react_busname,line_id=line_id,line_name=line_name,react_cap=react_cap,
                                                 react_id=react_id,convertible=convertible,rated_voltage=rated_voltage,reccmsndt=reccmsndt)
            msg = 'Reactor data saved successfully'
        reactordata = list(reactor.objects.filter(stn_name=stn_name,deleted=False).values())
        return JsonResponse({'msg':msg,'reactordata':reactordata})

class edit_reactor(View):
    def post(self, request):
        reactor_id = request.POST.get('reactor_id')
        try:
            reactor_obj = reactor.objects.get(id=reactor_id)
            response_data = {
                'id': reactor_obj.id,
                'react_type': reactor_obj.react_type,
                'react_voltage': reactor_obj.react_voltage,
                'react_bus': reactor_obj.react_bus,
                'react_busname': reactor_obj.react_busname,
                'line_id': reactor_obj.line_id,
                'line_name': reactor_obj.line_name,
                'react_cap': reactor_obj.react_cap,
                'react_id': reactor_obj.react_id,
                'convertible': reactor_obj.convertible,
                'rated_voltage': reactor_obj.rated_voltage,
                'reccmsndt': reactor_obj.reccmsndt,
            }
            return JsonResponse(response_data)
        except reactor.DoesNotExist:
            return JsonResponse({'error': 'Reactor data not found'}, status=404)

class delete_reactor(View):
    def post(self, request):
        reactor_id = request.POST.get('reactor_id')
        try:
            reactor_obj = reactor.objects.get(id=reactor_id)
            reactor_obj.deleted = True
            reactor_obj.save()
            return JsonResponse({'msg': 'Reactor data deleted successfully'})
        except reactor.DoesNotExist:
            return JsonResponse({'error': 'Reactor data not found'}, status=404)


class get_busnos(View):
    def get(self, request, *args, **kwargs):
        station_name = request.GET.get('station_name')
        voltage = request.GET.get('voltage')

        if station_name and voltage:
            bus_details = bus.objects.filter(stn_name=station_name, bus_volt=voltage, deleted=False).values('bus_no', 'bus_name')
            bus_list = list(bus_details)

            if bus_list:
                return JsonResponse({'status': 'success', 'bus_list': bus_list}, safe=False)
            else:
                return JsonResponse(
                    {'status': 'error', 'message': 'No bus numbers found for the selected station and voltage.'},
                    safe=False)

        return JsonResponse({'status': 'error', 'message': 'Invalid input. Please check the station name and voltage.'},
                            safe=False)

class save_lines(View):
    def post(self, request):
        lines_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        fbus_voltage = request.POST.get('fbus_voltage')
        fbus_no = request.POST.get('fbus_no')
        fbus_name = request.POST.get('fbus_name')
        toss_voltage = request.POST.get('toss_voltage')
        toss_name = request.POST.get('toss_name')
        to_busno = request.POST.get('to_busno')
        to_busname = request.POST.get('to_busname')
        to_length = request.POST.get('to_length')
        cktno = request.POST.get('cktno')
        category = request.POST.get('category')
        jursidiction = request.POST.get('jursidiction')
        linecmsndt = request.POST.get('linecmsndt')
        conductor_data = request.POST.get('conductor_data')
        pssc = request.POST.get('pssc')
        modifieddt = request.POST.get('modifieddt')

        cond_types = []
        cond_lengths = []

        if conductor_data:
            cond_data_pairs = conductor_data.split(', ')
            for pair in cond_data_pairs:
                if '-' in pair:
                    cond_type, cond_length = pair.split('-')
                    cond_types.append(cond_type.strip())
                    cond_lengths.append(cond_length.strip())

        cond_type_str = ','.join(cond_types)
        cond_length_str = ','.join(cond_lengths)

        if lines_id:
            try:
                lines_obj = lines.objects.get(id=lines_id)
                lines_obj.stn_name = stn_name
                lines_obj.fbus_voltage = fbus_voltage
                lines_obj.fbus_no = fbus_no
                lines_obj.fbus_name = fbus_name
                lines_obj.toss_voltage = toss_voltage
                lines_obj.toss_name = toss_name
                lines_obj.to_busno = to_busno
                lines_obj.to_busname = to_busname
                lines_obj.to_length = to_length
                lines_obj.cktno = cktno
                lines_obj.category = category
                lines_obj.jursidiction = jursidiction
                lines_obj.linecmsndt = linecmsndt
                lines_obj.cond_type = cond_type_str
                lines_obj.cond_length = cond_length_str
                lines_obj.modifieddt = modifieddt
                lines_obj.pssc = pssc

                lines_obj.save()
                msg = 'Lines details updated successfully'
            except lines.DoesNotExist:
                return JsonResponse({'error': 'Lines data not found'}, status=404)
        else:
            lines_obj = lines.objects.create(
                stn_name=stn_name, fbus_voltage=fbus_voltage, fbus_no=fbus_no,
                fbus_name=fbus_name, toss_voltage=toss_voltage, toss_name=toss_name,
                to_busno=to_busno, to_busname=to_busname, to_length=to_length,
                cktno=cktno, category=category, jursidiction=jursidiction,
                linecmsndt=linecmsndt, cond_type=cond_type_str, cond_length=cond_length_str, pssc=pssc,modifieddt=modifieddt
            )
            revelines_pssc = 'No' if pssc == 'Yes' else 'Yes'
            revelines_obj = lines.objects.create(stn_name=toss_name,fbus_voltage=toss_voltage,fbus_no=to_busno,
                                                 fbus_name=to_busname,toss_voltage=fbus_voltage,toss_name=stn_name,
                                                 to_busno=fbus_no,to_busname=fbus_name,to_length=to_length,cktno=cktno,
                                                 category=category,jursidiction=jursidiction,linecmsndt=linecmsndt,cond_type=cond_type_str,
                                                 cond_length=cond_length_str,pssc=revelines_pssc)
            msg = 'Lines details saved successfully'

        linesdata = list(lines.objects.filter(stn_name=stn_name,deleted=False).values())
        return JsonResponse({'msg': msg, 'linesdata': linesdata})


class edit_lines(View):
    def post(self, request):
        lines_id = request.POST.get('lines_id')
        try:
            lines_obj = lines.objects.get(id=lines_id)
            cond_types = lines_obj.cond_type.split(',') if lines_obj.cond_type else []
            cond_lengths = lines_obj.cond_length.split(',') if lines_obj.cond_length else []

            cond_data_pairs = [f"{t.strip()} - {l.strip()}" for t, l in zip(cond_types, cond_lengths)]
            cond_data_str = ', '.join(cond_data_pairs)

            response_data = {
                'id': lines_obj.id,
                'fbus_voltage': lines_obj.fbus_voltage,
                'fbus_no': lines_obj.fbus_no,
                'fbus_name': lines_obj.fbus_name,
                'toss_voltage': lines_obj.toss_voltage,
                'toss_name': lines_obj.toss_name,
                'to_busno': lines_obj.to_busno,
                'to_busname': lines_obj.to_busname,
                'to_length': lines_obj.to_length,
                'cktno': lines_obj.cktno,
                'category': lines_obj.category,
                'jursidiction': lines_obj.jursidiction,
                'linecmsndt': lines_obj.linecmsndt,
                'conductor_data': cond_data_str,
                'pssc':lines_obj.pssc,

            }
            return JsonResponse(response_data)
        except lines.DoesNotExist:
            return JsonResponse({'error': 'Lines data not found'}, status=404)

class delete_lines(View):
    def post(self, request):
        modifieddt = request.POST.get('modifieddt')
        lines_id = request.POST.get('lines_id')
        if lines_id is None:
            return JsonResponse({'error': 'Invalid line ID'}, status=400)
        try:
            lines_obj = lines.objects.get(id=lines_id)
            lines_obj.modifieddt = modifieddt
            lines_obj.deleted = True
            lines_obj.save()
            return JsonResponse({'msg': 'Lines data deleted successfully'})
        except lines.DoesNotExist:
            return JsonResponse({'error': 'Lines data not found'}, status=404)


