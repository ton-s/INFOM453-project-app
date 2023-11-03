from django.shortcuts import render

def room(request, room_name):


    return render(request, 'rooms/room.html', context={'room': room_name})

