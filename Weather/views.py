from django.shortcuts import render
from .service import get_weather


def main_page(request):
    if request.method == 'POST':
        city = request.POST['city']
        start_day = request.POST['start-date']
        end_day = request.POST['end-date']
        response = get_weather(city, start_day, end_day)
        if response == 'error':
            return render(request, 'Weather/main_page.html', {'error': 'Please check the data, it is entered incorrectly'})
        return render(request, 'Weather/result_page.html', {'weather_data': response})
    return render(request, 'Weather/main_page.html')

