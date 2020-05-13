
from django.http import HttpResponse
from django.shortcuts import render
from django.conf.urls import url, include
from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets

def homepage(request):
    return render(request, 'index.html')

def overview(request):
    return render(request, 'overview.html')