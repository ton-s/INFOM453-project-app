from django.contrib import admin

from rooms.models import Room

# Register the models
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Room, RoomAdmin)
