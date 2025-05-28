from django.contrib import admin

from .models import User, Hotel, HotelImage, HotelRoom, HotelReservation, HotelLocations, Flight

# Register your models here.

admin.site.register(User)
admin.site.register(Hotel)
admin.site.register(HotelImage)
admin.site.register(HotelRoom)
admin.site.register(HotelReservation)
admin.site.register(HotelLocations)
admin.site.register(Flight)
