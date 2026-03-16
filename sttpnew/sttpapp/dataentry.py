from datetime import date

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView

from .models import owner_master, district_master, zone_master, circle_master, div_master, subdiv_master, \
    substation_master, bus, transformer, capacitorbank, feeder, dgset, stntransformer, bulkloads, lines, reactor, \
    addedlines


class addition(View):
    def get(self, request):
        addedlinesdata = addedlines.objects.all()
        trfdata = transformer.objects.all()
        recdata = reactor.objects.all()
        capdata = capacitorbank.objects.all()
        bulkdata = bulkloads.objects.all()
        context = {'addedlinesdata': addedlinesdata, 'trfdata': trfdata, 'recdata': recdata, 'capdata': capdata,
                   'bulkdata': bulkdata}
        return render(request, 'addition.html', context)

class deletion(View):
    def get(self, request):
        substndata = substation_master.objects.all()
        context = {'substndata': substndata}
        return render(request, 'deletion.html', context)

    def post(self, request):
        # Handle search functionality
        if 'find' in request.POST:
            search_term = request.POST.get('stn_name')
            if search_term:
                data = substation_master.objects.filter(stn_name=search_term).first()
                if data:
                    trfdata = transformer.objects.filter(stn_name=search_term, deleted=False)
                    capdata = capacitorbank.objects.filter(stn_name=search_term, deleted=False)
                    bulkloadsdata = bulkloads.objects.filter(stn_name=search_term, deleted=False)
                    linesdata = lines.objects.filter(stn_name=search_term, deleted=False)
                    reactordata = reactor.objects.filter(stn_name=search_term, deleted=False)

                    context = {
                        'stn_name': search_term,
                        'data': data,
                        'trfdata': trfdata,
                        'capdata': capdata,
                        'bulkloadsdata': bulkloadsdata,
                        'linesdata': linesdata,
                        'reactordata': reactordata
                    }
                else:
                    msg = 'No data found for the given station name'
                    context = {
                        'msg': msg,
                        'stn_name': search_term
                    }
                return render(request, 'deletion.html', context)

        # Handle transformer deletion via AJAX
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' and 'delete_transformer' in request.POST:
            trans_id = request.POST.get('id')
            transformer_obj = transformer.objects.filter(id=trans_id).first()

            if transformer_obj:
                transformer_obj.deleted = True
                transformer_obj.save()
                return JsonResponse({'success': True, 'message': 'Transformer deleted successfully'})
            else:
                return JsonResponse({'success': False, 'message': 'Transformer not found'}, status=404)
        else:
            return render(request,'deletion.html')

class delete_trf(View):
    def post(self,request):
        trans_id = request.POST.get('id')
        trfdata = transformer.objects.filter(id=trans_id).first()

        if trfdata:
            trfdata.deleted = True
            trfdata.save()

            return render(request,'deletion.html')




class dataentry(View):
    def get(self, request):
        deltrfdata = transformer.objects.filter(deleted=False, deldt=date.today())
        return render(request, 'dataentry.html', {'deltrfdata': deltrfdata})

    def post(self, request):
        deltrfdata = transformer.objects.filter(deleted=False, deldt=date.today())
        stn_name = request.POST.get('stn_name')
        voltages = ['400kv', '220kv', '132kv', '33kv', '11kv']

        # Initialize dictionaries to store data for each voltage level
        bus_data = {volt: [] for volt in voltages}
        line_data = {volt: [] for volt in voltages}
        trf_data = {volt: [] for volt in voltages}
        rec_data = {volt: [] for volt in voltages}
        cap_data = {volt: [] for volt in voltages}
        bulk_data = {volt: [] for volt in voltages}

        stnname_exists = substation_master.objects.filter(stn_name=stn_name).exists()

        if stnname_exists:
            for volt in voltages:
                # Populate data for each voltage level
                bus_data[volt] = list(bus.objects.filter(stn_name=stn_name, bus_volt__icontains=volt, deleted=False))
                line_data[volt] = list(lines.objects.filter(stn_name=stn_name,deleted=False).filter(Q(fbus_voltage__icontains=volt) | Q(toss_voltage__icontains=volt)))
                trf_data[volt] = list(transformer.objects.filter(stn_name=stn_name, deleted=False).filter(Q(prim_voltage__icontains=volt) | Q(sec_voltage__icontains=volt)))
                rec_data[volt] = list(reactor.objects.filter(stn_name=stn_name, react_voltage__icontains=volt, deleted=False))
                cap_data[volt] = list(capacitorbank.objects.filter(stn_name=stn_name,cap_voltage__icontains=volt))
                bulk_data[volt] = list(bulkloads.objects.filter(stn_name=stn_name, bus_volt__icontains=volt))

            context = {'stn_name': stn_name,'stnname_exists': stnname_exists,'voltages': voltages,'bus_data': bus_data,
                'trf_data': trf_data,'rec_data': rec_data, 'line_data':line_data, 'cap_data':cap_data,'bulk_data':bulk_data,
                       'deltrfdata': deltrfdata}
            return render(request, 'dataentry.html', context)
        else:
            msg = 'No data available for the given station name'
            return render(request, 'dataentry.html', {'msg': msg})


class addlines(View):
    def post(self,request):

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
        deldt = request.POST.get('deldt')
        approved = request.POST.get('approved')

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

        lines_obj = addedlines.objects.create(
            stn_name=stn_name, fbus_voltage=fbus_voltage, fbus_no=fbus_no,
            fbus_name=fbus_name, toss_voltage=toss_voltage, toss_name=toss_name,
            to_busno=to_busno, to_busname=to_busname, to_length=to_length,
            cktno=cktno, category=category, jursidiction=jursidiction,
            linecmsndt=linecmsndt, cond_type=cond_type_str, cond_length=cond_length_str, pssc=pssc,
            modifieddt=modifieddt, deldt=deldt, approved=approved
        )
        revelines_pssc = 'No' if pssc == 'Yes' else 'Yes'
        revelines_obj = addedlines.objects.create(stn_name=toss_name, fbus_voltage=toss_voltage, fbus_no=to_busno,
                                             fbus_name=to_busname, toss_voltage=fbus_voltage, toss_name=stn_name,
                                             to_busno=fbus_no, to_busname=fbus_name, to_length=to_length, cktno=cktno,
                                             category=category, jursidiction=jursidiction, linecmsndt=linecmsndt,
                                             cond_type=cond_type_str,cond_length=cond_length_str, pssc=revelines_pssc,
                                             deldt=deldt, approved=approved)
        msg = 'Lines details saved successfully'

        return render(request,'addition.html',{'msg':msg})