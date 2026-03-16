from django.db import models

# Create your models here.

class circle_master(models.Model):
    id = models.AutoField(primary_key=True)
    circle_name = models.TextField()
    circle_id = models.TextField()
    zone_id = models.TextField()

    class Meta:
        db_table = 'circle_master'

class zone_master(models.Model):
    id = models.AutoField(primary_key=True)
    zone_name = models.TextField()
    zone_id = models.TextField()

    class Meta:
        db_table = 'zone_master'

class div_master(models.Model):
    id = models.AutoField(primary_key=True)
    div_name = models.TextField()
    div_id = models.TextField()
    circle_id = models.TextField()
    zone_id = models.TextField()

    class Meta:
        db_table = 'div_master'


class subdiv_master(models.Model):
    id = models.AutoField(primary_key=True)
    subdiv_name = models.TextField()
    subdiv_id = models.TextField()
    div_id = models.TextField()
    circle_id = models.TextField()
    zone_id = models.TextField()

    class Meta:
        db_table = 'subdiv_master'

class district_master(models.Model):
    id = models.AutoField(primary_key=True)
    dist_name = models.TextField()

    class Meta:
        db_table = 'district_master'

class owner_master(models.Model):
    id = models.AutoField(primary_key=True)
    owner_code = models.TextField()
    owner_name = models.TextField()

    class Meta:
        db_table = 'owner_master'

class substation_master(models.Model):
    id = models.AutoField(primary_key=True)
    short_name = models.TextField()
    stn_name = models.TextField()
    district = models.TextField()
    voltages = models.TextField()
    commission_dt = models.DateField()
    owner_list = models.TextField()
    owner_code = models.TextField()
    zone = models.TextField()
    circle = models.TextField()
    division = models.TextField()
    sub_div = models.TextField()
    lattitude = models.TextField()
    longitude = models.TextField()
    ssid = models.TextField()
    construction = models.TextField()
    updated_dt = models.DateField()
    remarks = models.TextField()

    class Meta:
        db_table = 'substation_master'

class bus(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    bus_no = models.TextField()
    bus_code = models.TextField()
    bus_name = models.TextField()
    bus_volt = models.TextField()

    class Meta:
        db_table = 'bus'

class transformer(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    trf_type = models.TextField()
    trf_rating = models.TextField()
    trf_id = models.TextField()
    trf_title = models.TextField()
    prim_voltage = models.TextField()
    prim_busno = models.TextField()
    sec_voltage = models.TextField()
    sec_busno = models.TextField()
    prim_busname = models.TextField(default=None)
    sec_busname = models.TextField(default=None)

    class Meta:
        db_table = 'transformer'

class reactor(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    react_type = models.TextField()
    react_voltage = models.TextField()
    react_bus = models.TextField()
    react_busname = models.TextField()
    line_id = models.TextField()
    line_name = models.TextField()
    react_cap = models.TextField()
    react_id = models.TextField()
    convertible = models.TextField()
    rated_voltage = models.TextField()

    class Meta:
        db_table = 'reactor'

class capacitorbank(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    cap_voltage = models.TextField()
    bus_no = models.TextField()
    bus_name = models.TextField()
    cap_rating = models.TextField()
    cap_id = models.TextField()
    rated_voltage = models.TextField()

    class Meta:
        db_table = 'capacitorbank'

class lines(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    fbus_voltage = models.TextField()
    fbus_no = models.TextField()
    fbus_name = models.TextField()
    toss_voltage = models.TextField()
    toss_name = models.TextField()
    to_busno = models.TextField()
    to_busname = models.TextField()
    to_length = models.TextField()
    cktno = models.TextField()
    category = models.TextField()
    jursidiction = models.TextField()
    cond_type = models.TextField()
    cond_length = models.TextField()

    class Meta:
        db_table = 'lines'


class feeder(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    voltage = models.TextField()
    bus_no = models.TextField()
    bus_name = models.TextField()
    feeder_no = models.TextField()
    feeder_name = models.TextField()
    otherend = models.TextField()
    connectiontype = models.TextField()
    cat_loads = models.TextField()
    autoload_shed = models.TextField()

    class Meta:
        db_table = 'feeder'


class genstation(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    gen_type = models.TextField()
    owner = models.TextField()
    stn_id = models.TextField()
    genstn_name = models.TextField()
    bus_voltage = models.TextField()
    bus_id = models.TextField()
    bus_name = models.TextField()
    noofwtg = models.TextField()
    wtg_cap = models.TextField()
    total_cap = models.TextField()
    station_name = models.TextField()
    gridbus_volt = models.TextField()
    tobus_name = models.TextField()
    tobus_no = models.TextField()
    stage = models.TextField()
    unit_no = models.TextField()
    unit_cap = models.TextField()
    grid_ss = models.TextField()
    noof_inv = models.TextField()
    inv_cap = models.TextField()
    dc_cap =models.TextField()

    class Meta:
        db_table = 'genstation'


class dgset(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    dgset_id = models.TextField()
    availability = models.TextField()
    rating = models.TextField()

    class Meta:
        db_table = 'dgset'

class stntransformer(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    prim_volt = models.TextField()
    sec_volt = models.TextField()
    rating = models.TextField()
    source = models.TextField()
    stntrf_id = models.TextField()
    trnf_id = models.TextField()
    teritory_volt = models.TextField()
    feeder_name = models.TextField()
    discomss = models.TextField()
    length_feeder = models.TextField()
    feed_type = models.TextField()
    feed_vol = models.TextField()
    bus_id = models.TextField()
    trftype = models.TextField()

    class Meta:
        db_table = 'stntransformer'


class bulkloads(models.Model):
    id = models.AutoField(primary_key=True)
    stn_name = models.TextField()
    bus_volt = models.TextField()
    bus_no = models.TextField()
    bus_name = models.TextField()
    cons_name = models.TextField()
    cons_cat = models.TextField()
    discom = models.TextField()
    contr_load = models.TextField()


    class Meta:
        db_table = 'bulkloads'











