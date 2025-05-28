from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import account_view, hotel_search, custom_password_reset_confirm, hotel_detail, book_now, booking_success
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('register/', views.register, name='register'),
    path('register_success/', views.register_success, name='register_success'),
    path('login/', views.login_view, name='login'),
    path('my_account', views.account_view, name='my_account'),
    path('logout/', views.user_logout, name='logout'),
    path('tos/', views.terms_of_service, name='tos'),
    path('privacy/', views.privacy_policy, name='privacy'),
    path('update-image/', account_view, name="update_profile_image"),
    path('hotel-search/', hotel_search, name="hotel_search"),
    path("reset_password/", auth_views.PasswordResetView.as_view(template_name='password_reset/password_reset_form.html'), name="reset_password"),
    path("reset_password_sent/", auth_views.PasswordResetDoneView.as_view(template_name='password_reset/password_reset_done.html'), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", custom_password_reset_confirm, name="password_reset_confirm"),
    path("reset_password_complete/", auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name="password_reset_complete"),
    path('hotel/<int:hotel_id>/', hotel_detail, name='hotel_detail'),
    path('book-now/<int:hotel_id>/<int:room_id>/', views.book_now, name='book_now'),
    path('booking-success/<int:reservation_id>/', views.booking_success, name='booking_success'),
    path('booking-success/', views.booking_success, name='booking_success'),
    path('process_payment/', views.process_payment, name='process_payment'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('process_payment/<int:reservation_id>/', views.process_payment, name='process_payment'),
    path('subscribe_newsletter/', views.subscribe_newsletter, name='subscribe_newsletter'),
     path('flights/', views.flight_list, name='flight_list'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)