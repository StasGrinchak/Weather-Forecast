from __future__ import print_function
import swagger_client
from datetime import datetime, timedelta
from swagger_client.rest import ApiException
from django.core.serializers import serialize
import json
import os
from .models import WeatherForTheDay


# configure API key authorization
configuration = swagger_client.Configuration()
configuration.api_key['key'] = os.environ.get('WEATHER_TOKEN')

# create an instance of the API class
api_instance = swagger_client.APIsApi(swagger_client.ApiClient(configuration))


def check_records_in_db(city: str, start_date: str, end_date: str):
    # checking if all records exist in our database

    try:
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")

        current_date = start_date
        records_exist = True

        print(start_date)

        while current_date <= end_date and records_exist:
            exists = WeatherForTheDay.objects.filter(day=current_date, city=city).exists()

            if not exists:
                records_exist = False
                break
            current_date += timedelta(days=1)

        if records_exist:
            return WeatherForTheDay.objects.filter(day__range=(start_date, end_date), city=city)
        else:
            return None
    except:
        return None


def get_weather(city: str, start_date: str, end_date: str):
    try:
        # history API
        check_records = check_records_in_db(city, start_date, end_date)
        if check_records is None:
            api_response = api_instance.history_weather(city, start_date, end_dt=end_date, unixend_dt=56, hour=24, lang='en')

            new_structure = [
                {
                    'date': forecast['date'],
                    'max_temp': forecast['day']['maxtemp_c'],
                    'min_temp': forecast['day']['mintemp_c'],
                    'avg_temp': forecast['day']['avgtemp_c'],
                    'avg_humidity': forecast['day']['avghumidity'],
                    'condition_text': forecast['day']['condition']['text'],
                    'icon_url': forecast['day']['condition']['icon'],
                }
                for forecast in api_response['forecast']['forecastday']
            ]

            for forecast_data in new_structure:
                date_str = forecast_data['date']
                date = datetime.strptime(date_str, '%Y-%m-%d').date()

                if not WeatherForTheDay.objects.filter(day=date, city=city).exists():
                    WeatherForTheDay.objects.create(
                        day=date,
                        city=city,
                        max_temp=forecast_data['max_temp'],
                        min_temp=forecast_data['min_temp'],
                        avg_temp=forecast_data['avg_temp'],
                        condition_text=forecast_data['condition_text'],
                        icon_url=forecast_data['icon_url'],
                        avg_humidity=forecast_data['avg_humidity']
                    )

            return new_structure
        else:
            json_data = serialize('json', check_records)
            data_list = json.loads(json_data)
            new_format_list = []
            for item in data_list:
                fields = item["fields"]
                new_format_item = {
                    'date': fields['day'],
                    'max_temp': fields['max_temp'],
                    'min_temp': fields['min_temp'],
                    'avg_temp': fields['avg_temp'],
                    'avg_humidity': fields['avg_humidity'],
                    'condition_text': fields['condition_text'],
                    'icon_url': fields['icon_url']
                }
                new_format_list.append(new_format_item)
            return new_format_list
    except ApiException as e:
        return 'error'