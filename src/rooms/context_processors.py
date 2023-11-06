from .models import Room


def room_list(request):
    rooms = Room.objects.all()

    return {'room_list': rooms}
