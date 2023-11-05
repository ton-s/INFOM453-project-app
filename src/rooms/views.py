from django.shortcuts import render

def room(request, slug):


    return render(request, 'rooms/room.html', context={})

