from .models import Room


def room_list(request):
    rooms = Room.objects.all()

    return {'rooms': rooms}
