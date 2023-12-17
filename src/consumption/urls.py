from django.urls import path

from consumption.views import heating_consumption, electric_consumption

urlpatterns = [
    path('electric-consumption/', electric_consumption, name='electric_consumption'),
    path('heating-consumption/', heating_consumption, name='heating_consumption'),
]
