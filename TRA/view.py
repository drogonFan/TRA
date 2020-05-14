
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from data.models import Record
from django.views.decorators.csrf import csrf_exempt
import json
import datetime

def homepage(request):
    return render(request, 'index.html')

def overview(request):
    return render(request, 'overview.html')

def heatmap(request):
    return render(request, 'heatmap.html')

@csrf_exempt
def add_data_2017(request):
    if request.method == 'POST':
        # openid = request.POST.get('openid', default='')
        # university = request.POST.get('university', default='')
        datas = json.loads(request.body.decode('utf-8'))
        print(datas)
        record = Record(ttype=datas[0], pickup_datetime=datetime.strptime(datas[1], '%Y-%m-%d %H:%M:%S'), 
                dropoff_datetime=datetime.strptime(datas[2], '%Y-%m-%d %H:%M:%S'), 
                passenger_count=datas[3], PULocationID=datas[4], DOLocationID=datas[5], 
                payment_type=datas[6], trip_distance=datas[7],
                fare_amount=datas[8], extra=datas[9],
                total_amount=datas[10])
        record.save()