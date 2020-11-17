from django.conf import settings
import json
import requests
from datetime import datetime,timedelta

class Weather():
    def __init__(self):

        #En este constructor se recupera la clave para realizar las peticiones en la URL
        self.api_key = settings._API_KEY_WEATHER


    #Función que hace la petición a la API
    def search(self, City='Mexico', Country='mx'):
        '''Recibe como parametros la ciudad y el pais, previamente se valida si los datos no estan vacios'''

        url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s&appid=%s"%(City,Country,self.api_key)
        response = requests.get(url)
        # Transforma los datos de la respuesta de la url a formato JSON
        data = json.loads(response.text)
        
        # si la respuesta de los datos no fue satisfactoria levanta un error
        if data['cod'] == 200:
            data = Weather().build_the_response(data)
        else: raise ValueError('Ingresa ciudad o pais válido')

        return data



    #Función donde se crea la estructura de los datos de respuesta,
    def build_the_response(self, data):
        '''Se reciben como datos los parametros self y data, donde data es el objeto en JSON
        dado de lo recuperado de la API del clima'''

        wt = Weather()
        response = {
            'location_name':data['name'] +' , '+ str(data['sys']['country']).lower(),
            'temperature':str(wt.kelvin_to_celcius(data['main']['temp']))+' °C',
            'wind': str(data['wind']['speed']) + ' m/s',
            'cloudiness':str(data['weather'][0]['description']).capitalize(),
            'pressure': str(data['main']['pressure'])+ ' hpa',
            'humidity':str(data['main']['humidity']) + '%',
            'sunrise': wt.transform_unix_to_cst(data['sys']['sunrise']),
            'sunset': wt.transform_unix_to_cst(data['sys']['sunset']),
            'geo_coordinates': '['+ str(data['coord']['lat'])+', ' + str(data['coord']['lon']) +']',
            'requested_time':datetime.now().strftime('%H:%M:%S')
        }
        return response

    def transform_unix_to_cst(self, hour):
        '''Transforma las horas que viene en formato unix a utc'''

        hour = int(hour)
        #se hace la resta por 21600 ya que representa UTC-6 y con esto tenemos la hora exata del centro
        hour = hour - 21600 

        #no transforma hora en negativos ni en cero
        if(hour != 0):
            hour = datetime.utcfromtimestamp(hour).strftime('%H:%M:%S')
            # hour = timezone('US/Central').localize(hour)

        return hour

    #función que transforma los grados de kelvin a celcius
    def kelvin_to_celcius(self,temp):
        temp = float(temp)
        celcius = temp - 273.15

        return round(celcius,2)