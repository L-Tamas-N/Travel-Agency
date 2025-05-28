from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from .forms import UserRegistrationFrom, UserChangeProfileImage, UserUpdateProfileInfo, PasswordResetForm
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, get_user_model, update_session_auth_hash
from django.contrib.auth.hashers import make_password
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import logout
from .models import Hotel, HotelReservation, HotelLocations, HotelRoom, Flight
from .scripts import extract_city_from_list
from datetime import datetime, date
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
import folium, random, string
from django.core.mail import send_mail
from django.utils import timezone
import json, requests, stripe


# Create your views here.
def homepage(request):
    return render(request, 'homepage/home.html')

def register(request):
    # Handle form submission if the request method is POST
    if request.method == 'POST':
        form = UserRegistrationFrom(request.POST)

        if form.is_valid():
            # Create user object without saving to DB yet
            user = form.save(commit=False)

            # Hash the password before saving
            user.password = make_password(user.password)

            # Save the user to the database
            form.save()

            # Redirect to login page after successful registration
            return redirect('login')
        else:
            # Extract specific error for the email field, if any
            email_error = None
            if form.errors.get('email'):
                email_error = form.errors.get('email')[0]

            # Re-render the form with validation errors
            return render(request, 'register/register.html', {
                'form': form,
                'email_error': email_error
            })

    else:
        # If not a POST request, just show the empty registration form
        form = UserRegistrationFrom()
    return render(request, 'register/register.html', {'form': form})

def register_success(request):
    return render(request, 'register_success/register-success.html')

def login_view(request):
    # Handle login form submission
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # Authenticate user with provided credentials
        user = authenticate(request, email=email, password=password)

        if user is not None:
            # Log the user in and redirect to home page
            auth_login(request, user)
            return redirect('http://127.0.0.1:8000/')
        else:
            # Invalid credentials; re-render login with error message
            return render(request, 'login/login.html', {'error': 'Invalid email or password'})
    return render(request, 'login/login.html')

@login_required
def account_view(request):
    user = request.user # Get the currently logged-in user
    password_error = None  # Track password mismatch error

    if request.method == 'POST':
         # Handle profile info update form
        form_info = UserUpdateProfileInfo(request.POST, instance=user)
        if form_info.is_valid():
            form_info.save()

        # Handle profile image update form
        form_image = UserChangeProfileImage(request.POST, request.FILES, instance=user)
        if form_image.is_valid():
            form_image.save()

         # Handle password change
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        password_error = None

        if password and confirm_password:
            if password == confirm_password:
                user.password = make_password(password)
                user.save()
            else:
                password_error = "Passwords do not match." # Display error on missmatch

        return render(request, 'my_account/my_account.html', {
            'form_info': form_info,
            'form_image': form_image,
            'user': user,
            'reservations': HotelReservation.objects.filter(user=user),
            'password_error': password_error
        })

    else:
        # For GET requests, load forms with current user data
        form_info = UserUpdateProfileInfo(instance=user)
        form_image = UserChangeProfileImage(instance=user)

    reservations = HotelReservation.objects.filter(user=user)

    return render(request, 'my_account/my_account.html', {
        'form_info': form_info,
        'form_image': form_image,
        'user': user,
        'reservations': reservations,
        'password_error': None
    })


def user_logout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/')

def terms_of_service(request):
    return render(request , 'TOS/tos.html')

def privacy_policy(request):
    return render(request, 'TOS/privacy.html')

def hotel_search(request):
    hotels = Hotel.objects.none()  # Start with an empty queryset

    if request.GET:
        hotels = Hotel.objects.all()

        # Get search parameters from the request
        location = request.GET.get('location')
        check_in = request.GET.get('check-in')
        check_out = request.GET.get('check-out')
        room_type = request.GET.get('rooms')

        # Filter hotels by location
        if location:
            hotels = hotels.filter(location__icontains=location)

        # Try to parse the check-in and check-out dates
        try:
            check_in_date = datetime.strptime(check_in, '%Y-%m-%d').date() if check_in else None
            check_out_date = datetime.strptime(check_out, '%Y-%m-%d').date() if check_out else None
        except ValueError:
            check_in_date, check_out_date = None, None  # If dates are invalid

        # Get all available rooms
        available_rooms = HotelRoom.objects.all()

        # Filter rooms by room type
        if room_type:
            available_rooms = available_rooms.filter(room_type__iexact=room_type)

        # Exclude rooms that are already reserved in the selected date range
        if check_in_date and check_out_date:
            unavailable_rooms = HotelReservation.objects.filter(
                check_in_date__lt=check_out_date,
                check_out_date__gt=check_in_date
            ).values_list("room", flat=True)

            available_rooms = available_rooms.exclude(id__in=unavailable_rooms)

        # Filter hotels that have at least one available room
        hotel_ids = available_rooms.values_list('hotel_id', flat=True)
        hotels = hotels.filter(id__in=hotel_ids).distinct()

    # Render the hotel list page with the filtered hotels
    return render(request, 'hotels/hotel_list.html', {'hotels': hotels})

User = get_user_model()

def custom_password_reset_confirm(request, uidb64, token):
    try:
        # Decode the user ID from base64
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError):
        user = None

    # Check if the token is valid for the user
    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")  
            confirm_password = request.POST.get("confirm_password")

            # Check if both passwords are provided
            if password and confirm_password:
                if password == confirm_password:
                    user.password = make_password(password)  # Hash and set new password
                    user.save()
                    messages.success(request, "Your password has been successfully reset.")
                    return redirect("password_reset_complete")  # Redirect after success
                else:
                    messages.error(request, "Passwords do not match.")  # Show mismatch error
        return render(request, "password_reset/password_reset_confirm.html")
    return render(request, "password_reset/password_reset_invalid.html")
    
def hotel_detail(request, hotel_id):
    # Get the hotel object or return 404 if not found
    hotel = get_object_or_404(Hotel, id=hotel_id)

    # Convert amenities string into a list
    amenities_list = hotel.amenities.split(",") if hotel.amenities else []

    # Get the hotel's location (only the first one if multiple exist)
    hotel_location = HotelLocations.objects.filter(hotel=hotel).first()

    # Create a map centered on the hotel's location
    if hotel_location:
        m = folium.Map(location=[hotel_location.latitude, hotel_location.longitude], zoom_start=15)
        folium.Marker([hotel_location.latitude, hotel_location.longitude], popup=hotel.name).add_to(m)
    else:
        m = folium.Map(location=[0, 0], zoom_start=9)  # Default location if no hotel location is found

    # Render the map as HTML for embedding in template
    map_html = m._repr_html_()

    # Get flights matching the hotel location
    flights = Flight.objects.filter(destination_city__icontains=hotel.location)

    return render(request, 'hotel_detail/hotel_detail.html', {
        'hotel': hotel,
        'amenities_list': amenities_list,
        'map_html': map_html,
        'flights': flights
    })
    
#Random password generator for automatic account creation
def generate_random_password(length=10):
    chars = string.ascii_letters + string.digits + "!@#$%^&*()"
    return "".join(random.choice(chars) for _ in range(length))

def book_now(request, hotel_id, room_id):
    # Get the hotel or return 404 if not found
    hotel = get_object_or_404(Hotel, id=hotel_id)

    if request.method == "GET":
        # Extract dates from GET parameters
        check_in_date = request.GET.get("check_in_date")
        check_out_date = request.GET.get("check_out_date")
        rooms = []

        if check_in_date and check_out_date:
            # Convert strings to date objects
            check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
            check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()

            # Validate dates
            if check_in_date_obj < date.today():
                return render(request, "booking/booking.html", {
                    "hotel": hotel,
                    "error_message": "Check-in date cannot be in the past.",
                    "check_in_date": check_in_date,
                    "check_out_date": check_out_date
                })

            if check_out_date_obj <= check_in_date_obj:
                return render(request, "booking/booking.html", {
                    "hotel": hotel,
                    "error_message": "Check-out date must be after check-in date.",
                    "check_in_date": check_in_date,
                    "check_out_date": check_out_date
                })

            # Find available rooms that are not booked for the given dates
            all_rooms = HotelRoom.objects.filter(hotel=hotel)

            for room in all_rooms:
                overlapping_reservations = HotelReservation.objects.filter(
                    room=room,
                    check_in_date__lt=check_out_date_obj,
                    check_out_date__gt=check_in_date_obj
                )
                if not overlapping_reservations.exists():
                    rooms.append(room)

        # Render booking page with available rooms
        return render(request, "booking/booking.html", {
            "hotel": hotel,
            "rooms": rooms,
            "check_in_date": check_in_date,
            "check_out_date": check_out_date
        })

    elif request.method == "POST":
        # Extract posted data
        check_in_date = request.POST.get("check_in_date")
        check_out_date = request.POST.get("check_out_date")
        selected_room_id = request.POST.get("room_id")

        # Get selected room or return 404
        selected_room = get_object_or_404(HotelRoom, id=selected_room_id, hotel=hotel)

        # Convert dates
        check_in_date_obj = datetime.strptime(check_in_date, "%Y-%m-%d").date()
        check_out_date_obj = datetime.strptime(check_out_date, "%Y-%m-%d").date()

        # Validate dates again
        if check_in_date_obj < date.today():
            return render(request, "booking/booking.html", {
                "hotel": hotel,
                "error_message": "Check-in date cannot be in the past.",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            })

        if check_out_date_obj <= check_in_date_obj:
            return render(request, "booking/booking.html", {
                "hotel": hotel,
                "error_message": "Check-out date must be after check-in date.",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            })

        # Check for conflicting reservations
        conflict = HotelReservation.objects.filter(
            room=selected_room,
            check_in_date__lt=check_out_date_obj,
            check_out_date__gt=check_in_date_obj
        ).exists()

        if conflict:
            return render(request, "booking/booking.html", {
                "hotel": hotel,
                "error_message": "This room is no longer available for the selected dates.",
                "check_in_date": check_in_date,
                "check_out_date": check_out_date
            })

        # Calculate total price based on number of nights
        num_nights = (check_out_date_obj - check_in_date_obj).days
        total_price = selected_room.price_per_night * num_nights

        # If user is not logged in, create a user account based on the email
        if not request.user.is_authenticated:
            email = request.POST.get("email")
            if email:
                password = generate_random_password()
                user, created = User.objects.get_or_create(email=email, defaults={
                    "first_name": "",
                    "last_name": "",
                    "phone": "",
                    "birth_date": None,
                })
                if created:
                    user.set_password(password)
                    user.save()
                    # Send the credentials to the user's email
                    send_mail(
                        "Your New Account",
                        f"Your account has been created.\n\nEmail: {user.email}\nPassword: {password}",
                        "admin@example.com",
                        [user.email],
                        fail_silently=False,
                    )
                auth_login(request, user)
        else:
            user = request.user

        # Create a new reservation
        reservation = HotelReservation.objects.create(
            hotel=hotel,
            room=selected_room,
            user=user,
            check_in_date=check_in_date_obj,
            check_out_date=check_out_date_obj,
            status="Booked",
            total_price=total_price 
        )

        # Redirect to success page
        return redirect("booking_success", reservation_id=reservation.id)


def booking_success(request, reservation_id):
    reservation = get_object_or_404(HotelReservation, id=reservation_id)
    
    return render(request, 'booking/booking_success.html', {
        'reservation': reservation,
        'payment_status': 'You can choose to pay online or pay at checkout.'
    })

stripe.api_key = "sk_test_51RBBMWI0QjogqOe0yEaYCG71omBp5t4ARQYGeQyUBXpgVkI3hIlzt2FSLn69mkevGYQhpwSw0lQDlWequWIzS1aP00AnK7WOcJ"

def process_payment(request, reservation_id):
    if not request.user.is_authenticated:
        return JsonResponse({"error": "User not authenticated"}, status=400)

    try:
        reservation = HotelReservation.objects.filter(user=request.user, status="Booked", id=reservation_id).last()

        if not reservation:
            return JsonResponse({"error": "No active reservation found."}, status=404)

        if reservation.was_paid:
            return JsonResponse({"error": "This reservation has already been paid."}, status=400)

        room_price = int(reservation.total_price * 100)  

        # Create Stripe checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': f"Reservation for {reservation.hotel.name} - {reservation.room.room_type}",
                    },
                    'unit_amount': room_price,  
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url=request.build_absolute_uri(f'/payment_success/?reservation_id={reservation.id}'),
            cancel_url=request.build_absolute_uri('/payment/cancel/'),
        )

        return redirect(checkout_session.url)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
def payment_success(request):
    reservation_id = request.GET.get('reservation_id')

    if reservation_id:
        reservation = get_object_or_404(HotelReservation, id=reservation_id)
        reservation.was_paid = True  
        reservation.save() 

    return render(request, 'payment/success.html', {
        'reservation': reservation,
        'payment_status': 'Payment was successful.'
    })

MAILCHIMP_API_KEY = "7842cd301e59382d523a944a033f5c2b-us1"
MAILCHIMP_SERVER_PREFIX = "us1"
MAILCHIMP_LIST_ID = "3c0eff4008"

def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        
        if email:
            try:
                response = requests.post(
                    f'https://{MAILCHIMP_SERVER_PREFIX}.api.mailchimp.com/3.0/lists/{MAILCHIMP_LIST_ID}/members/',
                    auth=('apikey', MAILCHIMP_API_KEY),
                    json={
                        "email_address": email,
                        "status": "subscribed"
                    }
                )

                print("Mailchimp Response Status Code:", response.status_code)
                print("Mailchimp Response Content:", response.json())

                if response.status_code == 200:
                    return JsonResponse({"success": "Successfully subscribed!"})
                else:
                    return JsonResponse({"error": f"Failed to subscribe. Mailchimp Error: {response.json()}"})
            except requests.exceptions.RequestException as e:
                return JsonResponse({"error": f"Request failed: {str(e)}"})
        else:
            return JsonResponse({"error": "Please provide a valid email address."})

    return JsonResponse({"error": "Invalid request method."}, status=405)

def flight_list(request):
    flights = Flight.objects.all()
    return render(request, 'flight/flight.html', {'flights': flights})



            


