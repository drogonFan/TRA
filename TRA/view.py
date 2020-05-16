
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from data.models import Record
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime
import django.utils.timezone as timezone

def homepage(request):
    return render(request, 'index.html')

def overview(request):
    return render(request, 'overview.html')

def heatmap(request):
    return render(request, 'heatmap.html')

@csrf_exempt
def api(request):
    # 区域，起始时间，终止时间，粒度
    print(request.POST)
    print(request.POST['region'])
    print(request.POST['begindate'])
    print(request.POST['enddate'])
    print(request.POST['range'])

    data = [{'x':10,'y':10}, {'x':15, 'y':15}]
    rs = {'msg':"exist"}
    # return render(request, 'chart.html', {'List': json.dumps(data),})
    return HttpResponse(json.dumps(rs))

@csrf_exempt
def gen_index_data(request):
    if request.method == 'POST':
        # 区域，起始时间，终止时间，粒度
        region = int(request.POST['region'])
        begindate = datetime.strptime(request.POST['begindate'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        enddata = datetime.strptime(request.POST['enddate'] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        ran = int(request.POST['range'])
        rec = Record.objects.filter(PULocationID__exact(region)).filter(pickup_datetime__range(begindate, enddata)).values(pickup_datetime.hour).annotate(Count('pickup_datetime'))
        print(rec)
        for re in rec:
            pass
        if ran == 60:
            pass
        else:
            pass

        rs = {'code':100}
    else:
        rs = {'code':109,'msg':''}
    # 返回json格式数据
    return HttpResponse(json.dumps(rs))

@csrf_exempt
def add_data_2017(request):
    if request.method == 'POST':
        # openid = request.POST.get('openid', default='')
        # university = request.POST.get('university', default='')
        datas = json.loads(request.body.decode('utf-8'))
        print(datas)
        udate = datetime.strptime(datas[1], '%Y-%m-%d %H:%M:%S')
        ddate = datetime.strptime(datas[2], '%Y-%m-%d %H:%M:%S')
        udate = udate.replace(tzinfo=timezone.utc)
        ddate = ddate.replace(tzinfo=timezone.utc)

        record = Record(ttype=datas[0], pickup_datetime=udate, 
                dropoff_datetime=ddate, 
                passenger_count=datas[3], PULocationID=datas[4], DOLocationID=datas[5], 
                payment_type=datas[6], trip_distance=datas[7],
                fare_amount=datas[8], extra=datas[9],
                total_amount=datas[10])
        record.save()
    rs = {}
    return HttpResponse(json.dumps(rs))