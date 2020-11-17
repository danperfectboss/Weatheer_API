from django.shortcuts import render
from django.views.generic import TemplateView
from app_weather.logic import Weather
from rest_framework.views import APIView
from rest_framework.response import Response
'''Implementados para el uso de cache'''
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.core.cache import cache


'''Global variable'''
# Se define el tiempo que vivira el caché en este caso son 3 minutos
TIME_CACHE= 60*3

class WeatherView(APIView):
    
    # metodo get
    def get(self, request):
        '''#se reciben los parametros enviados desde la vista'''
        
        # Parametro para obtener la ciudad  
        City = str(request.GET.get('city')).capitalize()
        
        #parametro para obtener el pais
        Country = str(request.GET.get('country')).lower()

        # Si la ciudad y el pais vienen con datos entran
        if City and Country:
            
            # ingresa a la funcion de validación y creación de la cache
            obj = validate_and_create_cache(City,Country)
                
        # En caso de venir los datos vacios levanta un error que se plasma en el navegador
        else: raise ValueError('El campo de Ciudad y codigo de país deben de llevar datos')

        
        
        return Response({'Response':obj})
    
    

def indexView(request):
        return render(request,'index.html')  

def pretty_data_view(request):
    
    '''#se reciben los parametros enviados desde la vista'''
    
    # Parametro para obtener la ciudad  
    City = str(request.GET.get('city')).capitalize()
    
    #parametro para obtener el pais
    Country = str(request.GET.get('country')).lower()

    # Si la ciudad y el pais vienen con datos entran
    if City and Country:
        
        # ingresa a la funcion de validación y creación de la cache
        obj = validate_and_create_cache(City,Country)
            
    # En caso de venir los datos vacios levanta un error que se plasma en el navegador
    else: raise ValueError('El campo de Ciudad y codigo de país deben de llevar datos')

    return render(request, 'pretty_weather.html',{'data':obj})


def validate_and_create_cache(City, Country):
    #Valida si el cache viene con datos
    if cache.get('location_name') is not None:
        
        # divide el nombre del cache para obtener el nombre de la ciudad
        cache_city = cache.get('location_name').split(' ,')[0]
        
        #si la ciudad es igual a la ciudad ingresada es igual a la que 
        #tiene la cache, recupera los datos de la cache
        if cache_city == City:

            #se crea el objeto de tipo diccionario para obtener los datos por medio de las keys
            new_obj=[
                'location_name',
                'temperature',
                'wind',
                'cloudiness',
                'pressure',
                'humidity',
                'sunrise',
                'sunset',
                'geo_coordinates',
                'requested_time'
            ]
            
            #Se guarda en la variable obj los datos recuperados de la caché
            obj = cache.get_many(new_obj)
        
        else:
            # si no lo es crea un nuevo objeto y una nueva caché para la petición
            obj = Weather().search(City,Country)
            cache.set_many(obj , TIME_CACHE )

    # si el cache no viene con datos se crea el nuevo objeto 
    else: 
        # hace la peticion a la url de la API de clima pasando como parametros 
        # la ciudad y el pais
        obj = Weather().search(City,Country)

        #Se define la cache con el objeto y el tiempo de duración
        cache.set_many(obj , TIME_CACHE )

    return obj




    