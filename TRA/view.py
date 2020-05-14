
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from data.models import Record
from django.views.decorators.csrf import csrf_exempt
import json

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
        print(request.POST)
        print(datas)
    else:
        rs = {'code':109, 'des':'Not accepting post requests'}
    return HttpResponse(json.dumps(rs))