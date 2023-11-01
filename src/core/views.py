from django.shortcuts import render
import requests

def index(request):

    # key = "3448cb1dd62b9758038f490877c25fb6"
    # url = f"http://api.weatherstack.com/current?access_key={key}&query=Gedinne"
    #
    #
    # data = requests.get(url).json()
    #
    # print(data)

    return render(request, 'core/home.html')
