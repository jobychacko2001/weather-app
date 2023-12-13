from django.shortcuts import render
import requests
from .forms import CityForm

def index(request):
    if request.method == 'POST':
        form = CityForm(request.POST)
        if form.is_valid():
            city = form.cleaned_data['city']
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=efe36ab6ccd00d6c097ae983d8bee4d0&units=metric'
            response = requests.get(url).json()
            weather = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }
    else:
        form = CityForm()
        weather = {}

    context = {'weather': weather, 'form': form}
    return render(request, 'weather_app/index.html', context)