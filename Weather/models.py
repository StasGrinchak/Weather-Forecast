from django.db import models


class WeatherForTheDay(models.Model):

    day = models.DateField()
    city = models.CharField(max_length=100)
    condition_text = models.CharField(max_length=255)
    icon_url = models.CharField(max_length=200)
    max_temp = models.FloatField()
    min_temp = models.FloatField()
    avg_temp = models.FloatField()
    avg_humidity = models.FloatField()
