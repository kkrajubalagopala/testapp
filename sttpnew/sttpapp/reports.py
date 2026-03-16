import json
from io import BytesIO

import pandas as pd
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db.models import Q


from .models import owner_master, district_master, zone_master, circle_master, div_master, subdiv_master, \
    substation_master, bus, transformer, reactor, capacitorbank, lines, feeder, dgset, stntransformer, bulkloads


class reports(View):
    def get(self, request):
        # Fetch all necessary data for the initial page load
        context = {
            'ownerdata': owner_master.objects.all(),
            'distdata': district_master.objects.all(),
            'zonedata': zone_master.objects.all(),
            'circldata': circle_master.objects.all(),
            'divdata': div_master.objects.all(),
            'subdivdata': subdiv_master.objects.all(),
            'substndata': substation_master.objects.all(),
        }
        return render(request, 'reports.html', context)


    def post(self, request):

        ownerdata = owner_master.objects.all()
        distdata = district_master.objects.all()
        zonedata = zone_master.objects.all()
        circldata = circle_master.objects.all()
        divdata = div_master.objects.all()
        subdivdata = subdiv_master.objects.all()
        substndata = substation_master.objects.all()

        # Get filter values from the POST request
        filters = {}
        zone_name = request.POST.get('zone')
        circle_name = request.POST.get('circle')
        div_name = request.POST.get('division')
        subdiv_name = request.POST.get('sub_div')
        stn_name = request.POST.get('stn_name')
        voltage = request.POST.get('voltages')
        owner_name = request.POST.get('owner_list')
        dist_name = request.POST.get('district')


        # Apply filters to substation_master
        if zone_name and zone_name != 'ALL':
            filters['zone'] = zone_name
        if circle_name and circle_name != 'ALL':
            filters['circle'] = circle_name
        if div_name and div_name != 'ALL':
            filters['division'] = div_name
        if subdiv_name and subdiv_name != 'ALL':
            filters['sub_div'] = subdiv_name
        if stn_name:
            filters['stn_name__icontains'] = stn_name
        if voltage and voltage != 'ALL':
            filters['voltages__icontains'] = voltage
        if owner_name and owner_name != 'ALL':
            filters['owner_list'] = owner_name
        if dist_name and dist_name != 'ALL':
            filters['district'] = dist_name

        # Fetch substations based on the filters
        substnreports = substation_master.objects.filter(**filters)

        # Create a dictionary to group substation details by stn_name
        substn_dict = {}
        for substn in substnreports:
            stn = substn.stn_name
            if stn not in substn_dict:
                substn_dict[stn] = {
                    'zones': set(),
                    'circles': set(),
                    'divisions': set(),
                    'subdivs': set(),
                    'districts': set()
                }
            # Add unique zone, circle, etc., for the same stn_name
            substn_dict[stn]['zones'].add(substn.zone)
            substn_dict[stn]['circles'].add(substn.circle)
            substn_dict[stn]['divisions'].add(substn.division)
            substn_dict[stn]['subdivs'].add(substn.sub_div)
            substn_dict[stn]['districts'].add(substn.district)

        # Convert sets to comma-separated strings
        for stn, details in substn_dict.items():
            substn_dict[stn]['zones'] = ', '.join(details['zones'])
            substn_dict[stn]['circles'] = ', '.join(details['circles'])
            substn_dict[stn]['divisions'] = ', '.join(details['divisions'])
            substn_dict[stn]['subdivs'] = ', '.join(details['subdivs'])
            substn_dict[stn]['districts'] = ', '.join(details['districts'])

        # Fetch related bus data
        stn_names = substnreports.values_list('stn_name', flat=True)
        stnvoltages = substnreports.values('voltages').distinct().order_by('voltages')
        stnzone = substnreports.values('zone').distinct().order_by('zone')
        stncircle = substnreports.values('circle').distinct().order_by('circle')
        stndivision = substnreports.values('division').distinct().order_by('division')
        stnsub_div = substnreports.values('sub_div').distinct().order_by('sub_div')
        stndistrict = substnreports.values('district').distinct().order_by('district')


        bus_filter = {'stn_name__in': stn_names, 'deleted': False}
        if voltage and voltage != 'ALL':
            bus_filter['bus_volt__icontains'] = voltage  # Add voltage filter here

        busreports = bus.objects.filter(**bus_filter)
        buscode = busreports.values('bus_code').distinct().order_by('bus_code')
        busno = busreports.values('bus_no').distinct().order_by('bus_no')
        busvolt = busreports.values('bus_volt').distinct().order_by('bus_volt')
        trfreports = transformer.objects.filter(stn_name__in=stn_names, deleted=False)
        trffilters = trfreports.values('trf_type').distinct().order_by('trf_type')
        voltratio = trfreports.values('prim_voltage', 'sec_voltage').distinct()
        trfcapacity = trfreports.values('trf_rating').distinct()
        reactorreports = reactor.objects.filter(stn_name__in=stn_names, deleted=False)
        rectype = reactorreports.values('react_type').distinct()
        recvolt = reactorreports.values('react_voltage').distinct()
        recrating = reactorreports.values('react_cap').distinct()
        convertiable = reactorreports.values('convertible').distinct()
        capacitorreports = capacitorbank.objects.filter(stn_name__in=stn_names, deleted=False)
        capvolt = capacitorreports.values('cap_voltage').distinct()
        capbusname = capacitorreports.values('bus_name').distinct()
        linereports = lines.objects.filter(stn_name__in=stn_names, deleted=False)
        linevolt = linereports.values('fbus_voltage').distinct()
        feederreports = feeder.objects.filter(stn_name__in=stn_names, deleted=False)
        contype = feederreports.values('connectiontype').distinct()
        category = feederreports.values('cat_loads').distinct()
        dgsetreports = dgset.objects.filter(stn_name__in=stn_names, deleted=False)
        stntrfreports = stntransformer.objects.filter(stn_name__in=stn_names, deleted=False)
        rating = stntrfreports.values('rating').distinct().order_by('rating')
        source = stntrfreports.values('source').distinct().order_by('source')
        bulkloadreports = bulkloads.objects.filter(stn_name__in=stn_names, deleted=False)
        bulkvolt = bulkloadreports.values('bus_volt').distinct().order_by('bus_volt')
        discom = bulkloadreports.values('discom').distinct().order_by('discom')


        # Create a list of dictionaries to hold bus data and substation info
        bus_with_substation_info = []
        for bus_obj in busreports:
            stn_info = substn_dict.get(bus_obj.stn_name, {})
            bus_with_substation_info.append({
                'bus': bus_obj,
                'zone': stn_info.get('zones', ''),
                'circle': stn_info.get('circles', ''),
                'division': stn_info.get('divisions', ''),
                'sub_div': stn_info.get('subdivs', ''),
                'district': stn_info.get('districts', '')
            })
        zones = set(bus['zone'] for bus in bus_with_substation_info if bus['zone'])
        circle = set(bus['circle'] for bus in bus_with_substation_info if bus['circle'])
        division = set(bus['division'] for bus in bus_with_substation_info if bus['division'])
        sub_div = set(bus['sub_div'] for bus in bus_with_substation_info if bus['sub_div'])
        district = set(bus['district'] for bus in bus_with_substation_info if bus['district'])

        # Convert the set to a sorted list
        buszones = sorted(zones)
        buscircle = sorted(circle)
        busdivision = sorted(division)
        bussub_div = sorted(sub_div)
        busdistrict = sorted(district)

        trf_with_ss_info = []
        for trf_obj in trfreports:
            stn_info = substn_dict.get(trf_obj.stn_name, {})
            trf_with_ss_info.append({'transformer': trf_obj,
                'zone': stn_info.get('zones', ''),
                'circle': stn_info.get('circles', ''),
                'division': stn_info.get('divisions', ''),
                'sub_div': stn_info.get('subdivs', ''),
                'district': stn_info.get('districts', '')
            })
        zones = set(transformer['zone'] for transformer in trf_with_ss_info if transformer['zone'])
        circle = set(transformer['circle'] for transformer in trf_with_ss_info if transformer['circle'])
        division = set(transformer['division'] for transformer in trf_with_ss_info if transformer['division'])
        sub_div = set(transformer['sub_div'] for transformer in trf_with_ss_info if transformer['sub_div'])
        district = set(transformer['district'] for transformer in trf_with_ss_info if transformer['district'])

        # Convert the set to a sorted list
        trfzones = sorted(zones)
        trfcircle = sorted(circle)
        trfdivision = sorted(division)
        trfsub_div = sorted(sub_div)
        trfdistrict = sorted(district)

        rec_with_ss_info = []
        for rec_obj in reactorreports:
            stn_info = substn_dict.get(rec_obj.stn_name, {})
            rec_with_ss_info.append({'reactor': rec_obj,
                                     'zone': stn_info.get('zones', ''),
                                     'circle': stn_info.get('circles', ''),
                                     'division': stn_info.get('divisions', ''),
                                     'sub_div': stn_info.get('subdivs', ''),
                                     'district': stn_info.get('districts', '')
                                     })
        zones = set(reactor['zone'] for reactor in rec_with_ss_info if reactor['zone'])
        circle = set(reactor['circle'] for reactor in rec_with_ss_info if reactor['circle'])
        division = set(reactor['division'] for reactor in rec_with_ss_info if reactor['division'])
        sub_div = set(reactor['sub_div'] for reactor in rec_with_ss_info if reactor['sub_div'])
        district = set(reactor['district'] for reactor in rec_with_ss_info if reactor['district'])

        # Convert the set to a sorted list
        reczones = sorted(zones)
        reccircle = sorted(circle)
        recdivision = sorted(division)
        recsub_div = sorted(sub_div)
        recdistrict = sorted(district)

        cap_with_ss_info = []
        for cap_obj in capacitorreports:
            stn_info = substn_dict.get(cap_obj.stn_name, {})
            cap_with_ss_info.append({'capacitorbank': cap_obj,
                                     'zone': stn_info.get('zones', ''),
                                     'circle': stn_info.get('circles', ''),
                                     'division': stn_info.get('divisions', ''),
                                     'sub_div': stn_info.get('subdivs', ''),
                                     'district': stn_info.get('districts', '')
                                     })
        zones = set(capacitorbank['zone'] for capacitorbank in cap_with_ss_info if capacitorbank['zone'])
        circle = set(capacitorbank['circle'] for capacitorbank in cap_with_ss_info if capacitorbank['circle'])
        division = set(capacitorbank['division'] for capacitorbank in cap_with_ss_info if capacitorbank['division'])
        sub_div = set(capacitorbank['sub_div'] for capacitorbank in cap_with_ss_info if capacitorbank['sub_div'])
        district = set(capacitorbank['district'] for capacitorbank in cap_with_ss_info if capacitorbank['district'])

        # Convert the set to a sorted list
        capzones = sorted(zones)
        capcircle = sorted(circle)
        capdivision = sorted(division)
        capsub_div = sorted(sub_div)
        capdistrict = sorted(district)

        line_with_ss_info = []
        for line_obj in linereports:
            fstn_info = substn_dict.get(line_obj.stn_name, {})
            tostn_info = substn_dict.get(line_obj.toss_name, {})
            line_with_ss_info.append({'lines': line_obj,
                                     'fzone': fstn_info.get('zones', ''),
                                     'fcircle': fstn_info.get('circles', ''),
                                     'fdivision': fstn_info.get('divisions', ''),
                                     'fsub_div': fstn_info.get('subdivs', ''),
                                     'fdistrict': fstn_info.get('districts', ''),
                                      'tozone': tostn_info.get('zones', ''),
                                      'tocircle': tostn_info.get('circles', ''),
                                      'todivision': tostn_info.get('divisions', ''),
                                      'tosub_div': tostn_info.get('subdivs', ''),
                                      'todistrict': tostn_info.get('districts', '')
                                     })
        fzones = set(lines['fzone'] for lines in line_with_ss_info if lines['fzone'])
        fcircle = set(lines['fcircle'] for lines in line_with_ss_info if lines['fcircle'])
        fdivision = set(lines['fdivision'] for lines in line_with_ss_info if lines['fdivision'])
        fsub_div = set(lines['fsub_div'] for lines in line_with_ss_info if lines['fsub_div'])
        fdistrict = set(lines['fdistrict'] for lines in line_with_ss_info if lines['fdistrict'])

        tozones = set(lines['tozone'] for lines in line_with_ss_info if lines['tozone'])
        tocircle = set(lines['tocircle'] for lines in line_with_ss_info if lines['tocircle'])
        todivision = set(lines['todivision'] for lines in line_with_ss_info if lines['todivision'])
        tosub_div = set(lines['tosub_div'] for lines in line_with_ss_info if lines['tosub_div'])
        todistrict = set(lines['todistrict'] for lines in line_with_ss_info if lines['todistrict'])

        # Convert the set to a sorted list
        flinezones = sorted(fzones)
        flinecircle = sorted(fcircle)
        flinedivision = sorted(fdivision)
        flinesub_div = sorted(fsub_div)
        flinedistrict = sorted(fdistrict)

        tolinezones = sorted(tozones)
        tolinecircle = sorted(tocircle)
        tolinedivision = sorted(todivision)
        tolinesub_div = sorted(tosub_div)
        tolinedistrict = sorted(todistrict)

        fed_with_ss_info = []
        for fed_obj in feederreports:
            stn_info = substn_dict.get(fed_obj.stn_name, {})
            fed_with_ss_info.append({'feeder': fed_obj,
                                      'zone': stn_info.get('zones', ''),
                                      'circle': stn_info.get('circles', ''),
                                      'division': stn_info.get('divisions', ''),
                                      'sub_div': stn_info.get('subdivs', ''),
                                      'district': stn_info.get('districts', '')
                                      })
        zones = set(feeder['zone'] for feeder in fed_with_ss_info if feeder['zone'])
        circle = set(feeder['circle'] for feeder in fed_with_ss_info if feeder['circle'])
        division = set(feeder['division'] for feeder in fed_with_ss_info if feeder['division'])
        sub_div = set(feeder['sub_div'] for feeder in fed_with_ss_info if feeder['sub_div'])
        district = set(feeder['district'] for feeder in fed_with_ss_info if feeder['district'])

        # Convert the set to a sorted list
        fedzones = sorted(zones)
        fedcircle = sorted(circle)
        feddivision = sorted(division)
        fedsub_div = sorted(sub_div)
        feddistrict = sorted(district)

        dgset_with_ss_info = []
        for dg_obj in dgsetreports:
            stn_info = substn_dict.get(dg_obj.stn_name, {})
            dgset_with_ss_info.append({'dgset': dg_obj,
                                     'zone': stn_info.get('zones', ''),
                                     'circle': stn_info.get('circles', ''),
                                     'division': stn_info.get('divisions', ''),
                                     'sub_div': stn_info.get('subdivs', ''),
                                     'district': stn_info.get('districts', '')
                                     })
        zones = set(dgset['zone'] for dgset in dgset_with_ss_info if dgset['zone'])
        circle = set(dgset['circle'] for dgset in dgset_with_ss_info if dgset['circle'])
        division = set(dgset['division'] for dgset in dgset_with_ss_info if dgset['division'])
        sub_div = set(dgset['sub_div'] for dgset in dgset_with_ss_info if dgset['sub_div'])
        district = set(dgset['district'] for dgset in dgset_with_ss_info if dgset['district'])

        # Convert the set to a sorted list
        dgzones = sorted(zones)
        dgcircle = sorted(circle)
        dgdivision = sorted(division)
        dgsub_div = sorted(sub_div)
        dgdistrict = sorted(district)

        stntrf_with_ss_info = []
        for stntrf_obj in stntrfreports:
            stn_info = substn_dict.get(stntrf_obj.stn_name, {})
            stntrf_with_ss_info.append({'stntransformer': stntrf_obj,
                                       'zone': stn_info.get('zones', ''),
                                       'circle': stn_info.get('circles', ''),
                                       'division': stn_info.get('divisions', ''),
                                       'sub_div': stn_info.get('subdivs', ''),
                                       'district': stn_info.get('districts', '')
                                       })
        zones = set(stntransformer['zone'] for stntransformer in stntrf_with_ss_info if stntransformer['zone'])
        circle = set(stntransformer['circle'] for stntransformer in stntrf_with_ss_info if stntransformer['circle'])
        division = set(stntransformer['division'] for stntransformer in stntrf_with_ss_info if stntransformer['division'])
        sub_div = set(stntransformer['sub_div'] for stntransformer in stntrf_with_ss_info if stntransformer['sub_div'])
        district = set(stntransformer['district'] for stntransformer in stntrf_with_ss_info if stntransformer['district'])

        # Convert the set to a sorted list
        stntrfzones = sorted(zones)
        stntrfcircle = sorted(circle)
        stntrfdivision = sorted(division)
        stntrfsub_div = sorted(sub_div)
        stntrfdistrict = sorted(district)

        bulk_with_ss_info = []
        for bulk_obj in bulkloadreports:
            stn_info = substn_dict.get(bulk_obj.stn_name, {})
            bulk_with_ss_info.append({'bulkloads': bulk_obj,
                                        'zone': stn_info.get('zones', ''),
                                        'circle': stn_info.get('circles', ''),
                                        'division': stn_info.get('divisions', ''),
                                        'sub_div': stn_info.get('subdivs', ''),
                                        'district': stn_info.get('districts', '')
                                        })
        zones = set(bulkloads['zone'] for bulkloads in bulk_with_ss_info if bulkloads['zone'])
        circle = set(bulkloads['circle'] for bulkloads in bulk_with_ss_info if bulkloads['circle'])
        division = set(bulkloads['division'] for bulkloads in bulk_with_ss_info if bulkloads['division'])
        sub_div = set(bulkloads['sub_div'] for bulkloads in bulk_with_ss_info if bulkloads['sub_div'])
        district = set(bulkloads['district'] for bulkloads in bulk_with_ss_info if bulkloads['district'])

        # Convert the set to a sorted list
        bulkzones = sorted(zones)
        bulkcircle = sorted(circle)
        bulkdivision = sorted(division)
        bulksub_div = sorted(sub_div)
        bulkdistrict = sorted(district)

        context = {'selected_zone':zone_name,'selected_circle':circle_name,'selected_division':div_name,'selected_sub_div':subdiv_name,
                   'selected_stn_name':stn_name,'selected_voltage':voltage,'selected_owner_name':owner_name,'selected_dist_name':dist_name,
                   'ownerdata':ownerdata,'distdata': distdata,'zonedata': zonedata,'circldata': circldata,'divdata': divdata,'subdivdata': subdivdata,
                   'substndata': substndata,'bus_with_substation_info': bus_with_substation_info,'trf_with_ss_info':trf_with_ss_info,'buscode':buscode,
                   'busno':busno,'substnreports':substnreports,'reactorreports':reactorreports,'trffilters':trffilters,'trfreports':trfreports,
                    'buszones':buszones,'buscircle':buscircle,'busdivision':busdivision,'bussub_div':bussub_div,'busdistrict':busdistrict,
                   'busvolt':busvolt,'stnvoltages':stnvoltages,'stnzone':stnzone,'stncircle':stncircle,'stndivision':stndivision,
                   'stnsub_div':stnsub_div,'stndistrict':stndistrict,'voltratio':voltratio,'trfcapacity':trfcapacity,'trfzones':trfzones,
                   'trfcircle':trfcircle,'trfdivision':trfdivision,'trfsub_div':trfsub_div,'trfdistrict':trfdistrict,'rectype':rectype,'recvolt':recvolt,
                   'recrating':recrating,'convertiable':convertiable,'reczones':reczones,'reccircle':reccircle,'recdivision':recdivision,'recsub_div':recsub_div,
                   'recdistrict':recdistrict,'rec_with_ss_info':rec_with_ss_info,'capacitorreports':capacitorreports,'capvolt':capvolt,
                   'capbusname':capbusname,'capzones':capzones,'capcircle':capcircle,'capdivision':capdivision,'capsub_div':capsub_div,
                   'capdistrict':capdistrict,'cap_with_ss_info':cap_with_ss_info,'linereports':linereports,'linevolt':linevolt,
                   'line_with_ss_info':line_with_ss_info,'flinezones':flinezones,'flinecircle':flinecircle,'flinedivision':flinedivision,
                   'flinesub_div':flinesub_div,'flinedistrict':flinedistrict,'tolinezones':tolinezones,'tolinecircle':tolinecircle,'tolinedivision':tolinedivision,
                   'tolinesub_div':tolinesub_div,'tolinedistrict':tolinedistrict,'feederreports':feederreports,'contype':contype,'category':category,
                   'fed_with_ss_info':fed_with_ss_info,'fedzones':fedzones,'fedcircle':fedcircle,'feddivision':feddivision,'fedsub_div':fedsub_div,
                   'feddistrict':feddistrict,'dgsetreports':dgsetreports,'dgset_with_ss_info':dgset_with_ss_info,'dgzones':dgzones,
                   'dgcircle':dgcircle,'dgdivision':dgdivision,'dgsub_div':dgsub_div,'dgdistrict':dgdistrict,'stntrfreports':stntrfreports,
                   'rating':rating,'source':source,'stntrfzones':stntrfzones,'stntrfcircle':stntrfcircle,'stntrfdivision':stntrfdivision,
                   'stntrfsub_div':stntrfsub_div,'stntrfdistrict':stntrfdistrict,'stntrf_with_ss_info':stntrf_with_ss_info,
                   'bulkloadreports':bulkloadreports,'bulkvolt':bulkvolt,'discom':discom,'bulk_with_ss_info':bulk_with_ss_info,'bulkzones':bulkzones,
                   'bulkcircle':bulkcircle,'bulkdivision':bulkdivision,'bulksub_div':bulksub_div,'bulkdistrict':bulkdistrict,
        }

        return render(request, 'reports.html', context)

class stnfilters(View):
    def get(self, request):
        # Check if the request is for exporting to Excel
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'

        # Get the filter parameters from the request
        stn_volt = request.GET.get('voltages', '')
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q object for building dynamic queries
        substation_query = Q()

        # Build the substation query based on the selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)
        if stn_volt and stn_volt != 'ALL':
            substation_query &= Q(voltages=stn_volt)

        # Filter substations based on the dynamic query
        substnreports = substation_master.objects.filter(substation_query)

        # Prepare data to be returned as JSON or for Excel export
        results = []
        for data in substnreports:
            results.append({
                'stn_name': data.stn_name,
                'voltages': data.voltages,
                'owner_code': data.owner_code,
                'lattitude': data.lattitude,
                'longitude': data.longitude,
                'zone': data.zone,
                'circle': data.circle,
                'division': data.division,
                'sub_div': data.sub_div,
                'district': data.district,
            })

        # Export to Excel if requested
        if export_to_excel:
            return self.export_to_excel(results)

        # Return JSON response for regular data requests (AJAX or initial page load)
        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):

        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()

        # Write the DataFrame to an Excel file using pandas
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='substations')

        # Seek to the beginning of the stream
        output.seek(0)

        # Generate the HTTP response for Excel file download
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=substn_report.xlsx'
        return response

class busfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        bus_code = request.GET.get('bus_code', '')
        bus_no = request.GET.get('bus_no', '')
        bus_volt = request.GET.get('bus_volt', '')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        bus_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if bus_code:
            bus_query &= Q(bus_code=bus_code)
        if bus_no.isdigit():
            bus_query &= Q(bus_no=int(bus_no))  # Convert to integer if it's a digit
        if bus_volt:
            bus_query &= Q(bus_volt=bus_volt)

        # Final query to filter bus reports
        busreports = bus.objects.filter(bus_query, deleted=False)

        # Prepare the response data
        results = []
        for data in busreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'bus_no': data.bus_no,
                    'bus_code': data.bus_code,
                    'bus_name': data.bus_name,
                    'bus_volt': data.bus_volt,
                    'buscmsndt': data.buscmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='bus')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bus_report.xlsx'
        return response

class FilterTransformersView(View):
    def get(self, request):
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        trf_type = request.GET.get('trf_type', '')
        voltage_ratio = request.GET.get('voltage_ratio', '')
        trf_rating = request.GET.get('trf_rating', '')

        # Extract primary and secondary voltages from the combined voltage ratio
        prim_voltage, sec_voltage = '', ''
        if voltage_ratio:
            prim_voltage, sec_voltage = voltage_ratio.split(' / ')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a Q object for filtering transformers
        trf_query = Q(stn_name__in=stn_names)
        if trf_type:
            trf_query &= Q(trf_type=trf_type)
        if prim_voltage:
            trf_query &= Q(prim_voltage=prim_voltage)
        if sec_voltage:
            trf_query &= Q(sec_voltage=sec_voltage)
        if trf_rating:
            trf_query &= Q(trf_rating=int(trf_rating))


        # Filter transformers based on the query
        trfreports = transformer.objects.filter(trf_query, deleted=False)

        # Prepare the response data
        results = []
        for data in trfreports:
            substation_info = substation_master.objects.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'trf_type': data.trf_type,
                    'prim_voltage': data.prim_voltage,
                    'sec_voltage': data.sec_voltage,
                    'prim_busno': data.prim_busno,
                    'prim_busname': data.prim_busname,
                    'sec_busno': data.sec_busno,
                    'sec_busname': data.sec_busname,
                    'trf_title': data.trf_title,
                    'trf_rating': data.trf_rating,
                    'trf_id': data.trf_id,
                    'trfcmsndt': data.trfcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)


    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Transformers')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=transformers_report.xlsx'
        return response


class recfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        react_type = request.GET.get('react_type', '')
        react_voltage = request.GET.get('react_voltage', '')
        react_cap = request.GET.get('react_cap', '')
        convertible = request.GET.get('convertible','')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        rec_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if react_type:
            rec_query &= Q(react_type=react_type)
        if react_cap.isdigit():
            rec_query &= Q(react_cap=int(react_cap))  # Convert to integer if it's a digit
        if react_voltage:
            rec_query &= Q(react_voltage=react_voltage)
        if convertible:
            rec_query &= Q(convertible=convertible)

        # Final query to filter bus reports
        reactorreports = reactor.objects.filter(rec_query, deleted=False)

        # Prepare the response data
        results = []
        for data in reactorreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'react_type': data.react_type,
                    'react_cap': data.react_cap,
                    'react_voltage': data.react_voltage,
                    'convertible': data.convertible,
                    'react_bus' : data.react_bus,
                    'react_busname' : data.react_busname,
                    'react_id' : data.react_id,
                    'rated_voltage' : data.rated_voltage,
                    'line_id' : data.line_id,
                    'line_name' : data.line_name,
                    'reccmsndt': data.reccmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='reactor')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=reactor_report.xlsx'
        return response


class capfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        cap_voltage = request.GET.get('cap_voltage', '')
        bus_name = request.GET.get('bus_name', '')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        cap_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if cap_voltage:
            cap_query &= Q(cap_voltage=cap_voltage)

        if bus_name:
            cap_query &= Q(bus_name=bus_name)


        # Final query to filter bus reports
        capacitorreports = capacitorbank.objects.filter(cap_query, deleted=False)

        # Prepare the response data
        results = []
        for data in capacitorreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'cap_voltage': data.cap_voltage,
                    'bus_no': data.bus_no,
                    'bus_name': data.bus_name,
                    'cap_rating': data.cap_rating,
                    'cap_id' : data.cap_id,
                    'rated_voltage' : data.rated_voltage,
                    'capcmsndt': data.capcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='capacitor')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=capacitor_report.xlsx'
        return response

class linefilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        fbus_voltage = request.GET.get('fbus_voltage', '').strip()

        # Additional filters
        fzone = request.GET.get('fzone', '')
        fcircle = request.GET.get('fcircle', '')
        fdivision = request.GET.get('fdivision', '')
        fsub_div = request.GET.get('fsub_div', '')
        fdistrict = request.GET.get('fdistrict', '')

        tozone = request.GET.get('tozone', '')
        tocircle = request.GET.get('tocircle', '')
        todivision = request.GET.get('todivision', '')
        tosub_div = request.GET.get('tosub_div', '')
        todistrict = request.GET.get('todistrict', '')

        # Initialize Q objects for filtering
        fsubstation_query = Q()

        # Build the substation query based on selected filters
        if fzone and fzone != 'ALL':
            fsubstation_query &= Q(zone=fzone)
        if fcircle and fcircle != 'ALL':
            fsubstation_query &= Q(circle=fcircle)
        if fdivision and fdivision != 'ALL':
            fsubstation_query &= Q(division=fdivision)
        if fsub_div and fsub_div != 'ALL':
            fsubstation_query &= Q(sub_div=fsub_div)
        if fdistrict and fdistrict != 'ALL':
            fsubstation_query &= Q(district=fdistrict)

         # Initialize Q objects for filtering
        tosubstation_query = Q()

        # Build the substation query based on selected filters
        if tozone and tozone != 'ALL':
            tosubstation_query &= Q(zone=tozone)
        if tocircle and tocircle != 'ALL':
            tosubstation_query &= Q(circle=tocircle)
        if todivision and todivision != 'ALL':
            tosubstation_query &= Q(division=todivision)
        if tosub_div and tosub_div != 'ALL':
            tosubstation_query &= Q(sub_div=tosub_div)
        if todistrict and todistrict != 'ALL':
            tosubstation_query &= Q(district=todistrict)

        # Filter substations based on the query
        fsubstnreports = substation_master.objects.filter(fsubstation_query)
        tosubstnreports = substation_master.objects.filter(tosubstation_query)

        fstn_names = fsubstnreports.values_list('stn_name', flat=True)
        tostn_names = tosubstnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        line_query = Q(stn_name__in=fstn_names) & Q(stn_name__in=tostn_names)

        # Apply additional bus filters
        if fbus_voltage:
            line_query &= Q(fbus_voltage=fbus_voltage)



        # Final query to filter bus reports
        linereports = lines.objects.filter(line_query, deleted=False)

        # Prepare the response data
        results = []
        for data in linereports:
            fsubstation_info = fsubstnreports.filter(stn_name=data.stn_name).first()
            tosubstation_info = tosubstnreports.filter(stn_name=data.toss_name).first()

            results.append({
                    'stn_name': data.stn_name,
                    'fbus_voltage': data.fbus_voltage,
                    'fbus_no': data.fbus_no,
                    'fbus_name': data.fbus_name,
                    'toss_voltage': data.toss_voltage,
                    'toss_name' : data.toss_name,
                    'to_busno' : data.to_busno,
                    'to_busname': data.to_busname,
                    'to_length': data.to_length,
                    'cktno': data.cktno,
                    'category': data.category,
                    'jursidiction': data.jursidiction,
                    'cond_type': data.cond_type,
                    'cond_length': data.cond_length,
                    'linecmsndt': data.linecmsndt.strftime('%d-%m-%Y'),
                    'pssc': data.pssc,
                    'fzone': fsubstation_info.zone,
                    'fcircle': fsubstation_info.circle,
                    'fdivision': fsubstation_info.division,
                    'fsub_div': fsubstation_info.sub_div,
                    'fdistrict': fsubstation_info.district,
                    'tozone': tosubstation_info.zone,
                    'tocircle': tosubstation_info.circle,
                    'todivision': tosubstation_info.division,
                    'tosub_div': tosubstation_info.sub_div,
                    'todistrict': tosubstation_info.district,

            })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='lines')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=lines_report.xlsx'
        return response


class fedfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        connectiontype = request.GET.get('connectiontype', '')
        cat_loads = request.GET.get('cat_loads', '')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        fed_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if connectiontype:
            fed_query &= Q(connectiontype=connectiontype)

        if cat_loads:
            fed_query &= Q(cat_loads=cat_loads)


        # Final query to filter bus reports
        feederreports = feeder.objects.filter(fed_query, deleted=False)

        # Prepare the response data
        results = []
        for data in feederreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'voltage': data.voltage,
                    'bus_no': data.bus_no,
                    'bus_name': data.bus_name,
                    'feeder_no': data.feeder_no,
                    'feeder_name' : data.feeder_name,
                    'otherend' : data.otherend,
                    'connectiontype' : data.connectiontype,
                    'cat_loads' : data.cat_loads,
                    'autoload_shed' : data.autoload_shed,
                    'fedcmsndt': data.fedcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='feeder')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=feeder_report.xlsx'
        return response

class dgfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'


        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)



        # Final query to filter bus reports
        dgsetreports = dgset.objects.filter(deleted=False)

        # Prepare the response data
        results = []
        for data in dgsetreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'dgset_id': data.dgset_id,
                    'availability': data.availability,
                    'rating': data.rating,
                    'dgcmsndt': data.dgcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='dgset')

        output.seek(0)
        response = HttpResponse(output, content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=dgset_report.xlsx'
        return response

class stntrffilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        rating = request.GET.get('rating', '')
        source = request.GET.get('source', '')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        stntrf_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if rating:
            stntrf_query &= Q(rating=int(rating))

        if source:
            stntrf_query &= Q(source=source)


        # Final query to filter bus reports
        stntrfreports = stntransformer.objects.filter(stntrf_query, deleted=False)

        # Prepare the response data
        results = []
        for data in stntrfreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'prim_volt': data.prim_volt,
                    'sec_volt': data.sec_volt,
                    'rating': data.rating,
                    'source': data.source,
                    'stntrf_id' : data.stntrf_id,
                    'trnf_id' : data.trnf_id,
                    'ict_capacity' : data.ict_capacity,
                    'feeder_name' : data.feeder_name,
                    'discomss' : data.discomss,
                    'length_feeder' : data.length_feeder,
                    'feed_type' : data.feed_type,
                    'bus_id' : data.bus_id,
                    'trftype' : data.trftype,
                    'stntfcmsndt': data.stntfcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Write the DataFrame to Excel
            df.to_excel(writer, index=False, sheet_name='stntrf')

        output.seek(0)
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=stntrf_report.xlsx'
        return response

class bulkfilters(View):
    def get(self, request):
        # Get parameters from request
        export_to_excel = request.GET.get('export_to_excel', 'false').lower() == 'true'
        bus_volt = request.GET.get('bus_volt', '')
        discom = request.GET.get('discom', '')

        # Additional filters
        zone = request.GET.get('zone', '')
        circle = request.GET.get('circle', '')
        division = request.GET.get('division', '')
        sub_div = request.GET.get('sub_div', '')
        district = request.GET.get('district', '')

        # Initialize Q objects for filtering
        substation_query = Q()

        # Build the substation query based on selected filters
        if zone and zone != 'ALL':
            substation_query &= Q(zone=zone)
        if circle and circle != 'ALL':
            substation_query &= Q(circle=circle)
        if division and division != 'ALL':
            substation_query &= Q(division=division)
        if sub_div and sub_div != 'ALL':
            substation_query &= Q(sub_div=sub_div)
        if district and district != 'ALL':
            substation_query &= Q(district=district)

        # Filter substations based on the query
        substnreports = substation_master.objects.filter(substation_query)
        stn_names = substnreports.values_list('stn_name', flat=True)

        # Create a query for the bus table using the filtered substation names
        bulk_query = Q(stn_name__in=stn_names)

        # Apply additional bus filters
        if bus_volt:
            bulk_query &= Q(bus_volt=bus_volt)

        if discom:
            bulk_query &= Q(discom=discom)


        # Final query to filter bus reports
        bulkloadreports = bulkloads.objects.filter(bulk_query, deleted=False)

        # Prepare the response data
        results = []
        for data in bulkloadreports:
            substation_info = substnreports.filter(stn_name=data.stn_name).first()
            if substation_info:
                results.append({
                    'stn_name': data.stn_name,
                    'bus_volt': data.bus_volt,
                    'bus_no': data.bus_no,
                    'bus_name': data.bus_name,
                    'cons_name': data.cons_name,
                    'cons_cat' : data.cons_cat,
                    'discom' : data.discom,
                    'contr_load' : data.contr_load,
                    'bulkcmsndt': data.bulkcmsndt.strftime('%d-%m-%Y'),
                    'zone': substation_info.zone,
                    'circle': substation_info.circle,
                    'division': substation_info.division,
                    'sub_div': substation_info.sub_div,
                    'district': substation_info.district,
                })

        if export_to_excel:
            return self.export_to_excel(results)

        return JsonResponse(results, safe=False)

    def export_to_excel(self, data):
        # Add S.No. (serial number) to the data
        for idx, row in enumerate(data, start=1):
            row['S.No.'] = idx

        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(data)

        # Reorder columns to place 'S.No.' at the beginning
        cols = ['S.No.'] + [col for col in df.columns if col != 'S.No.']
        df = df[cols]  # Rearrange the columns

        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Write the DataFrame to Excel
            df.to_excel(writer, index=False, sheet_name='bulkloads')

        output.seek(0)
        response = HttpResponse(output,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename=bulk_report.xlsx'
        return response

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



