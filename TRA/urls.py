"""TRA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('homepage/', view.homepage),
    path('heatmap/', view.heatmap),
    path('overview/', view.overview),
    path('traffic_trend/', view.trend),
    path('heatmap/', view.heatmap),
    path('get_heat_data/', view.get_heat_data),
    path('api/', view.api),
    path('add_data_2017/', view.add_data_2017),
    path('gen_index_data/', view.gen_index_data),
    path('get_flyingline_data/', view.get_flyingline_data),
    path('add_data_2016/',view.add_data_2016),

    path('prediction/', view.prediction),
    path('get_pre_data/', view.get_pre_data),
]
