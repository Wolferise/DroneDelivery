from django.db import models

# Create your models here.


class BPLA(models.Model):
    board_number = models.CharField(max_length=10)
    type = models.CharField(max_length=10)
    capacity = models.SmallIntegerField(blank=True, null=True)
    speed = models.FloatField(blank=True, null=True)
    latitude = models.CharField(max_length=15, null=True)
    longitude = models.CharField(max_length=15, null=True)
    azimuth = models.FloatField(blank=True, null=True)
    departure_hub = models.IntegerField(blank=True, null=True)
    destination_hub = models.IntegerField(blank=True, null=True)
    lat_delta = models.FloatField(blank=True, null=True)
    long_delta = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'bpla'


class HUB(models.Model):
    type = models.CharField(max_length=10)
    workload = models.FloatField(blank=True, null=True)
    latitude = models.CharField(max_length=15, null=True)
    longitude = models.CharField(max_length=15, null=True)
    hub_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'hub'


class ORDER(models.Model):
    weight = models.FloatField(blank=True, null=True)
    cur_departure = models.ForeignKey(HUB, on_delete = models.CASCADE, related_name='cur_departure', null=True)
    cur_destination = models.ForeignKey(HUB, on_delete = models.CASCADE, related_name='cur_destination', null=True)
    bpla = models.ForeignKey(BPLA, on_delete=models.SET_NULL, null=True)
    track = models.TextField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    order_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'order'


class STATISTICS(models.Model):
    total_weight_delivered = models.FloatField(blank=True, null=True)
    current_uav_quantity = models.IntegerField(blank=True, null=True)
    total_distance_travelled = models.FloatField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'statistics'
