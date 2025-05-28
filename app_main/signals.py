from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import HotelReservation, HotelRoom

@receiver(post_delete, sender=HotelReservation)
def update_room_availability(sender, instance, **kwargs):
    room = instance.room
    room.available = True
    room.save()