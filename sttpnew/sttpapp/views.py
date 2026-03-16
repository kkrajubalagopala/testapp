from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.views.generic import TemplateView


from .models import owner_master, district_master, zone_master, circle_master, div_master, subdiv_master, \
    substation_master, bus, transformer, capacitorbank, feeder, dgset, stntransformer, bulkloads


# Create your views here.
class home(View):
    def get(self, request):
        ownerdata = owner_master.objects.all()
        distdata = district_master.objects.all()
        zonedata = zone_master.objects.all()
        circldata = circle_master.objects.all()
        divdata = div_master.objects.all()
        subdivdata = subdiv_master.objects.all()
        substndata = substation_master.objects.all()
        context = {'ownerdata': ownerdata,'distdata':distdata,'zonedata':zonedata,'circldata':circldata,'divdata':divdata,'subdivdata':subdivdata
                   ,'substndata':substndata}
        return render(request, 'mtoplogy.html', context)

class get_circles(View):
    def get(self,request, zone_id):
        circles = circle_master.objects.filter(zone_id=zone_id).values('id', 'circle_name', 'circle_id')
        return JsonResponse(list(circles), safe=False)

class get_div(View):
    def get(self,request, circle_id):
        divs = div_master.objects.filter(circle_id=circle_id).values('id', 'div_name', 'div_id')
        return JsonResponse(list(divs), safe=False)

class get_subdiv(View):
    def get(self,request, div_id):
        subdivs = subdiv_master.objects.filter(div_id=div_id).values('id', 'subdiv_name', 'subdiv_id')
        return JsonResponse(list(subdivs), safe=False)


class get_stnname(View):
    def get(self, request):
        ownerdata = owner_master.objects.all()
        distdata = district_master.objects.all()
        zonedata = zone_master.objects.all()
        circldata = circle_master.objects.all()
        divdata = div_master.objects.all()
        subdivdata = subdiv_master.objects.all()
        substndata = substation_master.objects.all()
        busdata = bus.objects.all()
        trfdata = transformer.objects.all()
        feederdata = feeder.objects.all()
        dgsetdata = dgset.objects.all()
        bulkloadsdata = bulkloads.objects.all()
        context = {'ownerdata': ownerdata,'distdata': distdata,'zonedata': zonedata,'circldata': circldata,'divdata': divdata,
                   'subdivdata': subdivdata,'substndata': substndata,'busdata':busdata,'trfdata':trfdata,'feederdata':feederdata,
                   'dgsetdata':dgsetdata}
        return render(request, 'mtoplogy.html', context)

    def post(self, request):
        ownerdata = owner_master.objects.all()
        distdata = district_master.objects.all()
        zonedata = zone_master.objects.all()
        circldata = circle_master.objects.all()
        divdata = div_master.objects.all()
        subdivdata = subdiv_master.objects.all()
        substndata = substation_master.objects.all()
        #busdata = bus.objects.all()
        trfdata = transformer.objects.all()
        #feederdata = feeder.objects.all()
        #dgsetdata = dgset.objects.all()
        search_term = request.POST.get('stn_name')
        station_id = request.POST.get('station_id')
        bus_id = request.POST.get('id')

        if 'find' in request.POST:
            if search_term:
                data = substation_master.objects.filter(stn_name=search_term).first()
                if data:
                    busdata = bus.objects.filter(stn_name=search_term)
                    trfdata = transformer.objects.filter(stn_name=search_term)
                    capdata = capacitorbank.objects.filter(stn_name=search_term)
                    feederdata = feeder.objects.filter(stn_name=search_term)
                    dgsetdata = dgset.objects.filter(stn_name=search_term)
                    stntrfdata = stntransformer.objects.filter(stn_name=search_term)
                    bulkloadsdata = bulkloads.objects.filter(stn_name=search_term)
                    selected_voltages = data.voltages.split(',') if data.voltages else []
                    context = {'stn_name': search_term,'ownerdata': ownerdata,'distdata': distdata,'zonedata': zonedata,'circldata': circldata,
                        'divdata': divdata,'subdivdata': subdivdata,'substndata': substndata,'data': data,'selected_voltages': selected_voltages,
                               'busdata':busdata,'trfdata':trfdata,'capdata':capdata,'feederdata':feederdata,'dgsetdata':dgsetdata,'stntrfdata':stntrfdata,
                               'bulkloadsdata':bulkloadsdata}
                else:
                    msg = 'No data found for the given station name'
                    context = {'ownerdata': ownerdata,'distdata': distdata,'zonedata': zonedata,'circldata': circldata,
                        'divdata': divdata,'subdivdata': subdivdata,'substndata': substndata,'msg': msg}
                return render(request, 'mtoplogy.html', context)

        if 'save' in request.POST or 'update' in request.POST:
            short_name = request.POST.get('short_name')
            stn_name = request.POST.get('stn_name')
            district = request.POST.get('district')
            voltages = request.POST.getlist('voltages')  # Get list of selected checkboxes
            voltages_str = ','.join(voltages)  # Convert list to comma-separated string
            commission_dt = request.POST.get('commission_dt')
            owner_list = request.POST.get('owner_list')
            owner_code = request.POST.get('owner_code')
            zone = request.POST.get('zone')
            circle = request.POST.get('circle')
            division = request.POST.get('division')
            sub_div = request.POST.get('sub_div')
            lattitude = request.POST.get('lattitude')
            longitude = request.POST.get('longitude')
            ssid = request.POST.get('ssid')
            construction = request.POST.get('construction')
            updated_dt = request.POST.get('updated_dt')
            remarks = request.POST.get('remarks')

            if 'update' in request.POST and station_id:
                station = substation_master.objects.get(id=station_id)
                station.short_name = short_name
                station.stn_name = stn_name
                station.district = district
                station.voltages = voltages_str
                station.commission_dt = commission_dt
                station.owner_list = owner_list
                station.owner_code = owner_code
                station.zone = zone
                station.circle = circle
                station.division = division
                station.sub_div = sub_div
                station.lattitude = lattitude
                station.longitude = longitude
                station.ssid = ssid
                station.construction = construction
                station.updated_dt = updated_dt
                station.remarks = remarks
                station.save()
                msg = 'Station details updated successfully'
            else:
                substation_master.objects.create(short_name=short_name,stn_name=stn_name,district=district,voltages=voltages_str,
                    commission_dt=commission_dt,owner_list=owner_list,owner_code=owner_code,zone=zone,circle=circle,division=division,
                    sub_div=sub_div,lattitude=lattitude,longitude=longitude,ssid=ssid,construction=construction,updated_dt=updated_dt,
                    remarks=remarks)
                msg = 'Station details saved successfully'

            substndata = substation_master.objects.all()
            context = {'msg': msg,'ownerdata': ownerdata,'distdata': distdata,'zonedata': zonedata,'circldata': circldata,
                'divdata': divdata,'subdivdata': subdivdata,'substndata': substndata,'trfdata':trfdata }
            return render(request, 'mtoplogy.html', context)


        if 'save_dgset' in request.POST:
            stn_name = request.POST.get('stn_name')
            dgset_id = request.POST.get('dgset_id')
            availability = request.POST.get('availability')
            rating = request.POST.get('rating')

            dgset_obj = dgset.objects.create(stn_name=stn_name,dgset_id=dgset_id,availability=availability,rating=rating)

            msg = 'DGset data saved successfully'
            dgsetdata = dgset.objects.filter(stn_name=stn_name)
            context = {'msg':msg,'dgset_obj':dgset_obj,'dgsetdata':dgsetdata,'stn_name':stn_name}
            return render(request,'mtoplogy.html',context)

        if 'save_stntrf' in request.POST:
            stn_name = request.POST.get('stn_name')
            prim_volt = request.POST.get('prim_volt')
            sec_volt = request.POST.get('sec_volt')
            rating = request.POST.get('rating')
            stntrf_id = request.POST.get('stntrf_id')
            source = request.POST.get('source')
            trnf_id = request.POST.get('trnf_id')
            teritory_volt = request.POST.get('teritory_volt')
            feeder_name = request.POST.get('feeder_name')
            discomss = request.POST.get('discomss')
            length_feeder = request.POST.get('length_feeder')
            feed_type = request.POST.get('feed_type')
            feed_vol = request.POST.get('feed_vol')
            bus_id = request.POST.get('bus_id')
            trftype = request.POST.get('trftype')

            stntrf_obj = stntransformer.objects.create(stn_name=stn_name,prim_volt=prim_volt,sec_volt=sec_volt,rating=rating,stntrf_id=stntrf_id,source=source,
                                                       trnf_id=trnf_id,teritory_volt=teritory_volt,feeder_name=feeder_name,discomss=discomss,length_feeder=length_feeder,
                                                       feed_type=feed_type,feed_vol=feed_vol,bus_id=bus_id,trftype=trftype)
            msg = 'Station Transformer data saved successfully'
            stntrfdata = stntransformer.objects.filter(stn_name=stn_name)
            context = {'msg':msg,'stntrf_obj':stntrf_obj,'stntrfdata':stntrfdata,'trfdata':trfdata,'stn_name':stn_name}
            return render(request,'mtoplogy.html',context)

        if 'save_bulkloads' in request.POST:
            stn_name = request.POST.get('stn_name')
            bus_volt = request.POST.get('bus_volt')
            bus_no = request.POST.get('bus_no')
            bus_name = request.POST.get('bus_name')
            cons_name = request.POST.get('cons_name')
            cons_cat = request.POST.get('cons_cat')
            discom = request.POST.get('discom')
            contr_load = request.POST.get('contr_load')

            bulkloads_obj = bulkloads.objects.create(stn_name=stn_name,bus_volt=bus_volt,bus_no=bus_no,bus_name=bus_name,cons_name=cons_name,
                                                     cons_cat=cons_cat,discom=discom,contr_load=contr_load)
            msg = 'Bulkloads data saved successfully'
            bulkloadsdata = bulkloads.objects.filter(stn_name=stn_name)
            context = {'msg':msg,'bulkloads_obj':bulkloads_obj,'bulkloadsdata':bulkloadsdata,'stn_name':stn_name}
            return render(request,'mtoplogy.html',context)


        return render(request, 'mtoplogy.html')


class save_bus(View):
    def post(self, request):
        bus_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        bus_no = request.POST.get('bus_no')
        bus_name = request.POST.get('bus_name')
        bus_code = request.POST.get('bus_code')
        bus_volt = request.POST.get('bus_volt')

        if bus_id:  # If bus_id is present, update the existing record
            try:
                bus_obj = bus.objects.get(id=bus_id)
                bus_obj.stn_name = stn_name
                bus_obj.bus_no = bus_no
                bus_obj.bus_code = bus_code
                bus_obj.bus_name = bus_name
                bus_obj.bus_volt = bus_volt
                bus_obj.save()
                msg = 'Bus details updated successfully'
            except bus.DoesNotExist:
                return JsonResponse({'error': 'Bus not found'}, status=404)
        else:  # Otherwise, create a new record
            bus_obj = bus.objects.create(stn_name=stn_name,bus_no=bus_no,bus_code=bus_code,bus_name=bus_name,bus_volt=bus_volt            )
            msg = 'Bus details saved successfully'
        busdata = list(bus.objects.filter(stn_name=stn_name).values())  # Convert queryset to list of dictionaries
        return JsonResponse({'msg': msg, 'busdata': busdata})


class edit_bus(View):
    def post(self, request):
        bus_id = request.POST.get('bus_id')
        try:
            bus_obj = bus.objects.get(id=bus_id)
            response_data = {
                'bus_no': bus_obj.bus_no,
                'bus_code': bus_obj.bus_code,
                'bus_name': bus_obj.bus_name,
                'bus_volt': bus_obj.bus_volt,
            }
            return JsonResponse(response_data)
        except bus.DoesNotExist:
            return JsonResponse({'error': 'Bus not found'}, status=404)

class delete_bus(View):
    def post(self, request):
        bus_id = request.POST.get('bus_id')
        try:
            bus_obj = bus.objects.get(id=bus_id)
            bus_obj.delete()
            return JsonResponse({'msg': 'Bus deleted successfully'})
        except bus.DoesNotExist:
            return JsonResponse({'error': 'Bus not found'}, status=404)


class save_trf(View):
    def post(self, request):
        trans_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        trf_type = request.POST.get('trf_type')
        trf_rating = request.POST.get('trf_rating')
        trf_id = request.POST.get('trf_id')
        trf_title = request.POST.get('trf_title')
        prim_voltage = request.POST.get('prim_voltage')
        prim_busno = request.POST.get('prim_busno')
        sec_voltage = request.POST.get('sec_voltage')
        sec_busno = request.POST.get('sec_busno')
        prim_busname = request.POST.get('prim_busname')
        sec_busname = request.POST.get('sec_busname')

        if trans_id:  # If trans_id is present, update the existing record
            try:
                trf_obj = transformer.objects.get(id=trans_id)
                trf_obj.stn_name = stn_name
                trf_obj.trf_type = trf_type
                trf_obj.trf_rating = trf_rating
                trf_obj.trf_id = trf_id
                trf_obj.trf_title = trf_title
                trf_obj.prim_voltage = prim_voltage
                trf_obj.prim_busno = prim_busno
                trf_obj.sec_voltage = sec_voltage
                trf_obj.sec_busno = sec_busno
                trf_obj.prim_busname = prim_busname
                trf_obj.sec_busname = sec_busname
                trf_obj.save()
                msg = 'Transformer details updated successfully'
            except transformer.DoesNotExist:
                return JsonResponse({'error': 'Transformer not found'}, status=404)
        else:  # Otherwise, create a new record
            trf_obj = transformer.objects.create(
                stn_name=stn_name, trf_type=trf_type, trf_rating=trf_rating,
                trf_id=trf_id, trf_title=trf_title,
                prim_voltage=prim_voltage, prim_busno=prim_busno,
                sec_voltage=sec_voltage, sec_busno=sec_busno,
                prim_busname=prim_busname, sec_busname=sec_busname
            )
            msg = 'Transformer details saved successfully'

        trfdata = list(transformer.objects.filter(stn_name=stn_name).values())
        return JsonResponse({'msg': msg, 'trfdata': trfdata})

class edit_trf(View):
    def post(self, request):
        trans_id = request.POST.get('trans_id')
        try:
            trf_obj = transformer.objects.get(id=trans_id)
            response_data = {
                'trf_type': trf_obj.trf_type,
                'trf_rating': trf_obj.trf_rating,
                'trf_id': trf_obj.trf_id,
                'trf_title': trf_obj.trf_title,
                'prim_voltage': trf_obj.prim_voltage,
                'prim_busno': trf_obj.prim_busno,
                'sec_voltage': trf_obj.sec_voltage,
                'sec_busno': trf_obj.sec_busno,
                'prim_busname': trf_obj.prim_busname,
                'sec_busname': trf_obj.sec_busname,
            }
            return JsonResponse(response_data)
        except transformer.DoesNotExist:
            return JsonResponse({'error': 'Transformer not found'}, status=404)

class delete_trf(View):
    def post(self, request):
        trans_id = request.POST.get('trans_id')
        try:
            trf_obj = transformer.objects.get(id=trans_id)
            trf_obj.delete()
            return JsonResponse({'msg': 'Transformer deleted successfully'})
        except transformer.DoesNotExist:
            return JsonResponse({'error': 'Transformer not found'}, status=404)

class save_cap(View):
    def post(self, request):
        capbnk_id = request.POST.get('id')
        stn_name = request.POST.get('stn_name')
        cap_voltage = request.POST.get('cap_voltage')
        bus_no = request.POST.get('bus_no')
        bus_name = request.POST.get('bus_name')
        cap_rating = request.POST.get('cap_rating')
        cap_id = request.POST.get('cap_id')
        rated_voltage = request.POST.get('rated_voltage')

        if capbnk_id:
            try:
                cap_obj = capacitorbank.objects.get(id=capbnk_id)
                cap_obj.stn_name = stn_name
                cap_obj.cap_voltage = cap_voltage
                cap_obj.bus_no = bus_no
                cap_obj.bus_name = bus_name
                cap_obj.cap_rating = cap_rating
                cap_obj.cap_id = cap_id
                cap_obj.rated_voltage = rated_voltage
                cap_obj.save()
                msg = 'Capacitor Bank data updated successfully'
            except capacitorbank.DoesNotExist:
                return JsonResponse({'error': 'Capacitor Bank data not found'}, status=404)
        else:
            cap_obj = capacitorbank.objects.create(
                stn_name=stn_name,
                cap_voltage=cap_voltage,
                bus_no=bus_no,
                bus_name=bus_name,
                cap_rating=cap_rating,
                cap_id=cap_id,
                rated_voltage=rated_voltage
            )
            msg = 'Capacitor Bank details saved successfully'

        capdata = list(capacitorbank.objects.filter(stn_name=stn_name).values())
        return JsonResponse({'msg': msg, 'capdata': capdata})

class edit_cap(View):
    def post(self, request):
        capbnk_id = request.POST.get('capbnk_id')
        try:
            cap_obj = capacitorbank.objects.get(id=capbnk_id)
            response_data = {
                'id': cap_obj.id,
                'cap_voltage': cap_obj.cap_voltage,
                'bus_no': cap_obj.bus_no,
                'bus_name': cap_obj.bus_name,
                'cap_rating': cap_obj.cap_rating,
                'cap_id': cap_obj.cap_id,
                'rated_voltage': cap_obj.rated_voltage,
            }
            return JsonResponse(response_data)
        except capacitorbank.DoesNotExist:
            return JsonResponse({'error': 'Capacitor Bank data not found'}, status=404)

class delete_cap(View):
    def post(self, request):
        capbnk_id = request.POST.get('capbnk_id')
        try:
            cap_obj = capacitorbank.objects.get(id=capbnk_id)
            cap_obj.delete()
            return JsonResponse({'msg': 'Capacitor Bank data deleted successfully'})
        except capacitorbank.DoesNotExist:
            return JsonResponse({'error': 'Capacitor Bank not found'}, status=404)


