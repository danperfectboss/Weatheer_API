from django.conf import settings
import json
import requests
from datetime import datetime,timedelta

class Weather():
    def __init__(self):
        self.api_key = settings._API_KEY_WEATHER


    def search(self, City='Mexico', Country='mx'):        
        url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s&appid=%s"%(City,Country,self.api_key)
        response = requests.get(url)
        data = json.loads(response.text)
        if data['cod'] == 200:
            data = Weather().build_the_response(data)
        else: raise ValueError('Ingresa ciudad valida')
        
        return data


        

    def build_the_response(self, data):
        wt = Weather()
        response = {
            'location_name':data['name'] +' , '+ str(data['sys']['country']).lower(),
            'temperature':str(wt.kelvin_to_celcius(data['main']['temp']))+' °C',
            'wind': str(data['wind']['speed']) + ' m/s',
            'cloudiness':str(data['weather'][0]['description']).capitalize(),
            'pressure': str(data['main']['pressure'])+ ' hpa',
            'humidity':str(data['main']['humidity']) + '%',
            'sunrise': wt.transform_unix_to_cst(data['sys']['sunrise']) + ' UTC',
            'sunset': wt.transform_unix_to_cst(data['sys']['sunset']) + ' UTC',
            'geo_coordinates': '['+ str(data['coord']['lat'])+', ' + str(data['coord']['lon']) +']',
            'requested_time':datetime.now().strftime('%H:%M:%S')
        }
        return response

    def transform_unix_to_cst(self, hour):
        hour = int(hour)
        if(hour != 0):
            hour = datetime.utcfromtimestamp(hour).strftime('%H:%M:%S')
            # hour = timezone('US/Central').localize(hour)


        return hour 

    def kelvin_to_celcius(self,temp):
        temp = float(temp)
        celcius = temp - 273.15

        return round(celcius,2)