from django.contrib import admin

from rooms.models import Room, Lighting, Heating, HomeAppliance, Notification, LightingData, HeatingData, \
    HomeApplianceData


# Register the models
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name',)


admin.site.register(Room, RoomAdmin)
admin.site.register(Lighting)
admin.site.register(LightingData)
admin.site.register(Heating)
admin.site.register(HeatingData)
admin.site.register(HomeAppliance)
admin.site.register(HomeApplianceData)
admin.site.register(Notification)
