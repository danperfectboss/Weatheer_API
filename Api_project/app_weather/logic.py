from django.conf import settings
import json
import requests

class Weather():
    def __init__(self):
        self.api_key = settings._API_KEY_WEATHER


    def search(self, City='Mexico', Country='mx'):        
        url = "https://api.openweathermap.org/data/2.5/weather?q=%s,%s&appid=%s"%(City,Country,self.api_key)
        response = requests.get(url)
        data = json.loads(response.text)
        print(data)
        
        return data
