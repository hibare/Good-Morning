import logging
from datetime import datetime
import pytz
from decouple import config
import requests
from geopy.geocoders import Nominatim

# Configure and create a logger
logging.basicConfig(format='%(asctime)s [%(filename)s:%(funcName)s:%(lineno)d] [%(levelname)s] %(name)s: %(message)s') 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) 

class OpenWeatherAPI:

    def __init__(self):
        self.API_KEY = config("OPEN_WEATHER_API")
        TIMEZONE = config("TIMEZONE")
        self.LOCAL_TZ = pytz.timezone(TIMEZONE)
    
    def __get_lan_lon(self, city, country):
        query = "%s, %s" % (city, country)

        geolocator = Nominatim(user_agent="GoodMorning")
        location = geolocator.geocode(query)

        return location.latitude, location.longitude



    def one_call(self, city, country):
        result = dict(
            status=False,
            weather=dict(
                current=dict(),
                hourly=list(),
                daily=list()
            ),
            error=None
        )
        
        try:
            lat, lon = self.__get_lan_lon(city, country)

            url = "https://api.openweathermap.org/data/2.5/onecall?appid=%s&lat=%s&lon=%s&exclude=minutely&units=metric" % (self.API_KEY, lat, lon)
            
            response = requests.get(url, timeout=60)
            j_response = response.json()

            current = dict(
                now=datetime.fromtimestamp(j_response.get("current").get("dt"), self.LOCAL_TZ).strftime("%d-%m-%Y %H-%M-%S"),
                temp=j_response.get("current").get("temp"),
                wind_speed=j_response.get("current").get("wind_speed"),
                weather=j_response.get("current").get("weather")[0].get("main"),
                description=j_response.get("current").get("weather")[0].get("description")
            )

            hourly = list()

            for _hourly in j_response.get("hourly")[::4]:
                hourly.append(dict(
                    hour=datetime.fromtimestamp(_hourly.get("dt"), self.LOCAL_TZ).strftime("%d-%H"),
                    temp=_hourly.get("temp"),
                    wind_speed=_hourly.get("wind_speed"),
                    weather=_hourly.get("weather")[0].get("main"),
                    description=_hourly.get("weather")[0].get("description")
                ))

            result.update(dict(
                status=True,
                weather=dict(
                    current=current,
                    hourly=hourly[:6]
                )
            ))
        except Exception:
            logger.exception("Exception in one call for lat=%s, lon=%s", lat, lon)
            result.update(
                error="Exception in request"
            )
        
        return result
