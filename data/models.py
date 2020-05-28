from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Record(models.Model):
    # lpep_pickup_datetime,lpep_dropoff_datetime,
    # PULocationID,DOLocationID,
    # passenger_count,trip_distance,fare_amount,
    # extra,total_amount,payment_type,trip_type,diff_time
    oid = models.AutoField(primary_key = True)
    ttype = models.CharField(max_length=2)
    pickup_datetime = models.DateTimeField('上车时间', default = timezone.now)
    dropoff_datetime = models.DateTimeField('上车时间', default = timezone.now)
    passenger_count = models.IntegerField()
    PULocationID = models.IntegerField()
    DOLocationID = models.IntegerField()
    payment_type = models.IntegerField()
    trip_distance = models.FloatField()
    fare_amount = models.FloatField()
    extra = models.FloatField()
    total_amount = models.FloatField()

    class Meta:
        db_table = 'nyc_taxi'

class OldRecord(models.Model):
    oid = models.AutoField(primary_key = True)
    ttype = models.CharField(max_length=2)
    pickup_datetime = models.DateTimeField('上车时间', default = timezone.now)
    dropoff_datetime = models.DateTimeField('上车时间', default = timezone.now)
    passenger_count = models.IntegerField()
    uplat = models.FloatField()
    uplon = models.FloatField()
    droplat = models.FloatField()
    droplon = models.FloatField()
    payment_type = models.IntegerField()
    trip_distance = models.FloatField()
    fare_amount = models.FloatField()
    extra = models.FloatField()
    total_amount = models.FloatField()

    class Meta:
        db_table = 'old_nyc_taxi'