from django.urls import path

from .views import consumption, heating_consumption, electric_consumption

urlpatterns = [
    path('consumption/', consumption, name='consumption'),
    path('heating-consumption/', heating_consumption, name='heating_consumption'),
    path('electric-consumption/', electric_consumption, name='electric_consumption')
]