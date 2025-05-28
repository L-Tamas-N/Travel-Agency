from django.db import models
from django.contrib.auth.models import UserManager, AbstractBaseUser, PermissionsMixin
from django.utils import timezone

# Create your models here.

class CustomUserManager(UserManager):
    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("A vaild email address is not provided.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)
    
    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email, password, **extra_fields)
    
# Custom User model 
class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(blank=True, default='', unique=True)
    first_name = models.CharField(blank=True, default='', max_length=150)
    last_name = models.CharField(blank=True, default='', max_length=150)
    phone = models.CharField(blank=True, default='', max_length=15)
    birth_date = models.DateField(blank=True, null=True)
    user_image = models.FileField(upload_to="media/uploads/", default="media/uploads/Default_user_img.png")

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_created = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_full_name(self):
        return self.first_name
    
    def get_short_name(self):
        return self.first_name or self.email.split('@')[0]
    
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    price_range_per_night = models.CharField(max_length=100)
    rating = models.IntegerField(default = 0)
    amenities = models.TextField(blank= True, null=True)
    address = models.CharField(max_length=255)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="media/hotels/")

    def __str__(self):
        return f"Image for {self.hotel.name}"
    
class HotelRoom(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="rooms")
    room_type = models.CharField(max_length=100)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    available = models.BooleanField(default=True)

    def __str__(self):
        return f"Room - {self.room_type} for {self.hotel.name}"
    
class HotelReservation(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room = models.ForeignKey(HotelRoom, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    status = models.CharField(max_length = 50, default="Booked")
    was_paid = models.BooleanField(default=False)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Reservation - {self.user} for {HotelRoom.room_type} on {self.check_in_date}"
    
class HotelLocations(models.Model):
    hotel = models.OneToOneField(Hotel, on_delete=models.CASCADE, related_name="location_details")
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return f"{self.hotel.name} - ({self.latitude}, {self.longitude})"
    
class Flight(models.Model):
    departure_city = models.CharField(max_length=255)
    destination_city = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    airline = models.CharField(max_length=255)
    duration = models.CharField(max_length=100)
    contact = models.CharField(max_length=255)

    def __str__(self):
        return f"Flight from {self.departure_city} to {self.destination_city}"