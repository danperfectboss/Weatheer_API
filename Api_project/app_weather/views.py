from django.shortcuts import render
from django.views.generic import TemplateView
from app_weather.logic import Weather
from rest_framework.views import APIView
from rest_framework.response import Response
'''Implementados para el uso de cache'''
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie


# Create your views here.

class WeatherView(APIView):
    @method_decorator(cache_page(60*4))
    @method_decorator(vary_on_cookie)
    def get(self, request):

        City = str(request.GET.get('city')).capitalize()
        Country = str(request.GET.get('country')).lower()

        if City and Country:
            obj = Weather().search(City,Country)
        else: raise ValueError('El campo de Ciudad y codigo de país deben de llevar datos')
        
        return Response({'Response':obj})
    
    

def indexView(request):
        return render(request,'index.html')  

