from django.contrib import admin

from rooms.models import Room, Device, Lighting, Heating, HomeAppliance, Notification

# Register the models
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Room, RoomAdmin)
admin.site.register(Device)
admin.site.register(Lighting)
admin.site.register(Heating)
admin.site.register(HomeAppliance)
admin.site.register(Notification)