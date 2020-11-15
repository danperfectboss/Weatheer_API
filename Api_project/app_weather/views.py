from django.shortcuts import render
from django.views.generic import TemplateView
from app_weather.logic import Weather
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class WeatherView(APIView):

    def get(self, request):

        City = str(request.GET.get('city')).capitalize()
        Country = str(request.GET.get('country')).lower()


        obj = Weather().search(City,Country)

        # return render(request,'index.html')
        return Response({'datac':obj})
    
    def indexView(TemplateView):
        template_name = "index.html"
        

