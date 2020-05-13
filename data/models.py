from django.db import models
import django.utils.timezone as timezone
# Create your models here.

class Record(models.Model):
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

    def __str__(self):
        return self.oid

    class Meta:
        db_table = 'nyc_taxi'
