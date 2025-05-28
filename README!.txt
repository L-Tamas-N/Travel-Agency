Project description

This is a simple booking (hotels) website application which uses at it's core Python 3.13 and Django.
For all technologies/libraries used please check requirments.txt

Make sure you have VS Code installed (or any IDE), MySQL https://dev.mysql.com/downloads/workbench/


Setup:

1.Create clone request: https://github.com/L-Tamas-N/Travel-Agency.git
2.Instal requirments: pip install -r requirements.txt
3.Create migrations: python manage.py migrate // python manage.py makemigrations
4.Check if server is running: python manage.py runserver

Create super user:
1. python manage.py createsuperuser
2. provide ex email: djangoadmin@djangoadmin.com
3. password ex: 12345
4. press y -> enter
5. access http://127.0.0.1:8000/admin/
6. use credentials

Features:

Find Flight -> Displays all available flights which the database currently holds (accessed by Find Flight button in header) or select Show Flights button under Flights section on homepage

Account registration:
1. Click sign up button on header.
2. Fill in form.
3. Log in

Booking:
a. Access hotels by:
  1.a: Click on Find Stays button on header
  2.a: Click Book Now button
  3.a: Select Location card under Plan your perfect trip section (note: Only Istanbul and Sydney are working currently)
  4.a: Show hotels button under Hotels section, homepage
b. Use filter to display available hotels (note only locations Isanbul and Sydney will display hotels)
c. Select Hotel
d. Click book now
e. Fill in with form with information
  1.e Provide burner email address suggested platform: https://temp-mail.org/en/
f. select room from dropdown
g. select pay now to proceed to checkout stripe
  1.g fill in with card information DO NOT PROVIDE REAL CARD DATA.... Stripe is in test mode so use following information for test:
        Card Number: 4242 4242 4242 4242
	MM/YY: 01/28
	CVC: 444
	Cardholder Name: Jon Doe
	Country: *Any country can be used

Update account information:
1. Access my account by clicking Welcome, *Yourname in header
2. Click red pen button under stock profile image to update profile image
3. fill in account form to update information
4. use Change Password form to update password

Account Booking Section:
You can check available reservations. After reservation if payment was not provided user can pay from here as well using the pay now button.

Automatic Account creation:
If reservation was made prior to log in an account is automatically created and login data is sent trough email. You can use https://temp-mail.org/en/ to test this. (tested with burner gmail account works as well)


Newsletter:
Add burner email to newsletter section(Homepage -> Above Footer section) . Confirmation message Json: {"success": "Successfully subscribed!"}
Log in to mailchimp with credentials below and check if email address was added.

MailChimp Credentials:
Tester credentials: djangotestprojectta@gmail.com
Password: R3HYHjv!!-PBwxQ

Additionaly you can create your own MailChimp account but make sure to update API information in views.py lines 457,458, 459

Conclusion:
The project is not perfect and not complete but the challange was to create a working desktop demo in 100h... After 120 hours these were the features I could implement.

Upcomiing:
In the future I will add the following features/fixes:
1. Responsive design.
2. Reservation: add persons not just room types
3. Update more data with more cities.
4. Additional mobile application.
5. Google Analytics



