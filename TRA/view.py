
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets
from data.models import Record
import json

def homepage(request):
    return render(request, 'index.html')

def overview(request):
    return render(request, 'overview.html')

def heatmap(request):
    return render(request, 'heatmap.html')

def add_data_2017(request):
    if request.method == 'POST':
        datas = json.loads(request.body.decode('utf-8'))
        print(datas)
    else:
        rs = {'code':109, 'des':'Not accepting post requests'}
    return HttpResponse(json.dumps(rs))