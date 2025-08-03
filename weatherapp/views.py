from multiprocessing import context
# from pyexpat.errors import messages
from django.contrib import messages
from django.shortcuts import render,HttpResponse
import requests
import datetime

# Create your views here.
def home(request):

    city = request.POST.get('city', 'Hyderabad')
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid=7306893296d240c5aa8f4661c6f07ab1'
    params = {'units': 'metric'}
    
    API_KEY = 'AIzaSyBXHndPiZ5OLn5ZICJV-uuJHkLmg8MeCzw'
    SEARCH_ENGINE_ID = '97ffbaf9d137a4a63'
    
    query = city + "1920*1080"
    page = 1
    start = (page-1)*10+1
    search_type = 'image'
    city_url = f"https://www.googleapis.com/customsearch/v1?key={API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}&searchType={search_type}&start={start}&imgSize=large"
    
    data = requests.get(city_url).json()
    count = 1
    search_item = data.get("items", [])
    image_url = search_item[1]['link'] if len(search_item) > 1 else None

    try:
        data = requests.get(url, params=params).json()
    
        description = data['weather'][0]['description']
        icon = data['weather'][0]['icon']
        temp = data['main']['temp']
    
        day = datetime.date.today()

        return render(request, 'weatherapp/home.html', {
            'city': city,
            'description': description,
            'icon': icon,
            'temp': temp,
            'day': day,
            'exception_occurred': False,
            'image_url': image_url
        })
    except:
        exception_occurred = True
        messages.error(request, "City not found. Please try again.")
        day = datetime.date.today()
        return render(request, 'weatherapp/home.html', {
            'city': "Hyderabad",
            'description': "Cloudy",
            'icon': '01d',
            'temp': '32',
            'day': day,
            'exception_occurred': True,
        })