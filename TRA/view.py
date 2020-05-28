
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from data.models import Record, OldRecord
from django.views.decorators.csrf import csrf_exempt
import json
from datetime import datetime, timedelta
import django.utils.timezone as timezone
from TRA.gginfos import gginfo_170,gginfo_230,gginfo_234, jiashuju
import copy
import random

def homepage(request):
    return render(request, 'index.html')

def overview(request):
    return render(request, 'overview.html')

def heatmap(request):
    return render(request, 'heatmap.html')

def trend(request):
    return render(request, 'traffic_trend.html')

def prediction(request):
    return render(request, 'prediction.html')

@csrf_exempt
def get_heat_data(request):
    if request.method == "POST":
        datalist = {0: [12, 24, 42, 45, 88, 116, 120, 127, 127, 128, 128, 152, 153, 194, 202, 209, 243, 244, 103, 104, 105], 1: [4, 
13, 41, 43, 74, 74, 74, 74, 74, 87, 125, 144, 148, 151, 158, 166, 211, 224, 232, 261], 2: [50, 75, 90, 100, 113, 114, 137, 140, 143, 164, 229, 231, 233, 233, 246, 249, 262, 262, 263], 3: [48, 68, 
79, 107, 141, 142, 161, 162, 163, 170, 186, 230, 234, 236, 237, 238, 239]}
        colorlist = ['#9AFF9A', '#00EE00', '#00CD00', '#008B00']
        rs = {'code':100, 'data':datalist, 'colorlist':colorlist}
    else:
        rs = {'code':109, 'data':datalist, 'colorlist':colorlist}
    return HttpResponse(json.dumps(rs))

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

def heat(request):
    if request.method == 'POST':
        begindate = datetime.strptime(request.POST['begindate'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        enddate = datetime.strptime(request.POST['enddate'] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        begindate = begindate.replace(tzinfo=timezone.utc)
        enddate = enddate.replace(tzinfo=timezone.utc)
        # rec = Record.objects.filter(pickup_datetime__range=(begindate, enddate))
        # # datalist, quartiles = cal(rec)
        datamap = {}
        for i in range(4):
            datamap[i] = []

        # for info, shape in zip(map.comarques_info, map.comarques):
        #     if info['borough'] == 'Manhattan':
        #         location_ID = info['LocationID']
        #         peo = datalist[location_ID]
        #         if peo < quartiles[0]:
        #             datamap[0].append(location_ID)
        #         elif peo < quartiles[1]:
        #             datamap[1].append(location_ID)
        #         elif peo < quartiles[2]:
        #             datamap[2].append(location_ID)
        #         else:
        #             datamap[3].append(location_ID)
        rs = {'code':100, 'data':datamap}
    else:
        # 不接受get请求
        rs = {'code':109, 'msg':''}
    # 返回json格式数据
    return HttpResponse(json.dumps(rs))


@csrf_exempt
def gen_index_data(request):
    if request.method == 'POST':
        # 区域，起始时间，终止时间，粒度
        region = int(request.POST['region'])

        # 从数据库中读取数据（根据区域以及时间限制）
        rec = Record.objects.filter(DOLocationID=region)
        weeklist = {}

        for i in range(7):
            hourlist = {}
            for j in range(24):
                hourlist[j] = 0
            weeklist[i] = hourlist
        
        # 统计数目
        for re in rec:
            week = re.pickup_datetime.weekday()
            weeklist[week][re.pickup_datetime.hour] += 1
        # 使用假数据测试
        weeklist = copy.deepcopy(jiashuju)
        for i in range(7):
            data = []
            for k,v in weeklist[i].items():
                data.append({'x':k, 'y':v})
            weeklist[i] = data
        
        if region == 170:
            gdata = gginfo_170
        elif region == 230:
            gdata = gginfo_230
        else:
            gdata = gginfo_234
        rs = {'code':100, 'data':weeklist, 'gdata':gdata}
    else:
        # 不接受get请求
        rs = {'code':109, 'msg':''}
    # 返回json格式数据
    return HttpResponse(json.dumps(rs))

@csrf_exempt
def get_flyingline_data(request):
    # 返回最近10秒钟所有的交通数据，以及今日的总人数
    if request.method == 'POST':
        data = json.loads(request.body)
        # 获取用户输入地点
        region = data['region']
        rec = OldRecord.objects.filter(ttype=region)[:30]
        startpoints = []
        endpoints = []
        for r in rec:
            startpoints.append([r.uplon, r.uplat])
            endpoints.append([r.droplon, r.droplat])
        rs = {'code':100, 'startpoints':startpoints, 'endpoints':endpoints}
    else:
        rs = {'code':109, 'msg':''}
    return HttpResponse(json.dumps(rs))

def deal_data(datalist):
    maxy = 0
    for data in datalist:
        if maxy < data['y']:
            maxy = data['t']
    for data in datalist:
        if data['y'] == maxy:
            data['y'] = 1
        else:
            data['y'] = data['y'] / maxy + random.randint(-100, 100) / 100
            if data['y'] > 1:
                data['y'] = 0.99
            elif data['y'] < 0:
                data['y'] = 0.01
    return datalist

@csrf_exempt
def get_pre_data(request):
    if request.method == 'POST':
        # 区域，起始时间，终止时间，粒度
        region = int(request.POST['region'])
        begindate = datetime.strptime(request.POST['begindate'] + ' 00:00:00', '%Y-%m-%d %H:%M:%S')
        enddate = datetime.strptime(request.POST['enddate'] + ' 23:59:59', '%Y-%m-%d %H:%M:%S')
        days = (enddate - begindate).days
        starttime = begindate + timedelta(days=-1)
        delta = timedelta(days=1)
        print(days)
        rs = {}
        for i in range(days):        
            # 使用假数据测试
            week = random.randint(0, 7)
            pre = []
            for k, v in jiashuju[i].items():
                pre.append({'x':k, 'y':v})
            starttime += delta
            rs[starttime.strftime('%Y-%m-%d')] = deal_data(pre)
        pre = []
        for k, v in jiashuju[0].items():
            pre.append({'x':k, 'y':v})
        predate = starttime.strftime('%Y-%m-%d')
        if True:
            labels = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
        else:
            labels = ['0:00', '1:00', '2:00', '3:00', '4:00', '5:00', '6:00', '7:00', '8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00', '22:00', '23:00']
        rs = {'code':100, 'chartdata':rs, 'predata':deal_data(pre),'predate':predate,'label':labels}
    else:
        # 不接受get请求
        rs = {'code':109, 'msg':''}
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

@csrf_exempt
def add_data_2016(request):
    if request.method == 'POST':
        # openid = request.POST.get('openid', default='')
        # university = request.POST.get('university', default='')
        datas = json.loads(request.body.decode('utf-8'))
        print(datas)
        udate = datetime.strptime(datas[1], '%Y-%m-%d %H:%M:%S')
        ddate = datetime.strptime(datas[2], '%Y-%m-%d %H:%M:%S')
        udate = udate.replace(tzinfo=timezone.utc)
        ddate = ddate.replace(tzinfo=timezone.utc)

        record = OldRecord(ttype=datas[0], pickup_datetime=udate, 
                dropoff_datetime=ddate, 
                passenger_count=datas[3], uplon=datas[4],uplat=datas[5],droplon=datas[6],droplat=datas[7], 
                payment_type=datas[8], trip_distance=datas[9],
                fare_amount=datas[10], extra=datas[11],total_amount=datas[12])
        record.save()
    rs = {}
    return HttpResponse(json.dumps(rs))