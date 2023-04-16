
# QuickPay Business App

This is a Backend side of a Business  application that allows businesses to manage their transactions and payments.

 This project is built with Django DRF, Djoser, and Postgres DB.


# Built With

>[Python](https://www.python.org/) - Programming language used

>[Django](https://www.djangoproject.com/) - Web framework used

>[Django Rest Framework](https://www.django-rest-framework.org/) - Toolkit used to build APIs

>[Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html) - Toolkit used to build authentication APIs

>[PostgreSQL](https://www.postgresql.org/) - Database used
# Installation

 Clone the project from GitHub:

    git clone https://github.com/baabbii69/QuickPay-BusinessApp.git




 Create a virtual environment and activate it:


    python3 -m venv venv
    venv\Scripts\activate
Install the project dependencies:

    pip install -r requirements.txt
Create the Postgres database:

    DB name: BusinessApp

    Update/Insert Your Password in Settings.py  in DATABASE Part
Run database migrations:

    python manage.py migrate 
Create a superuser:

    python manage.py createsuperuser

Start the development server:

    python manage.py runserver

# API Endpoints for Auth

Business App provides the following API endpoints:

> `/auth/users/` (POST):  creates  a new user by inserting a json file like below.


    {
        "email": "example@gmail.com",
        "first_name": "Joe",
        "last_name": "mama",
        "business_name": "Joemamajj",
        "password": "12345678",
        "re_password": "12345678"
    }

    after inserting this data You will receive an email with activation link like this :
    http://127.0.0.1:8000/activate/Mg/bmlxqo-47e3945cc65b9ba26d8c26e32390aec1
    
    Mg:    is your uid and 
    bmlxqo-47e3945cc65b9ba26d8c26e32390aec1:  is you activation token


> `auth/users/activation/` (POST): To Activate Your Account.


    {
	    "uid": "Mg",
	    "token": "bmlxqo-47e3945cc65b9ba26d8c26e32390aec1"
    }

> `/auth/jwt/create/` (POST): To Login and receive access and refresh token


    {
        "email": "example@gmail.com",
        "password": "12345678"
    }
    
    After You Login You will receive access and refresh token

> `/auth/jwt/refresh/` (POST): To get a new access when it expires by inputing the refresh token you got from Loging in


    {
       "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTY1OTYxNiwianRpIjoiMGE1NWQ3NjY3NTQ5NDE2N2IxYjQ4YWExMmQ3MDYxZDUiLCJ1c2VyX2lkIjoyfQ.PLFx-W_Z0vycWtoqlZd1KaF7vs5qCW1qkdgat92s07Q"
    }

> `/auth/users/reset_password/` (POST):  request password reset.


    {
        "email": "example@gmail.com"
    }

    after inserting this data You will receive an email saying you requested a password reset and will have a link like this :
    http://127.0.0.1:8000/password/reset/confirm/Mg/bmecjm-836936a57f2b488b0b5848ef9ab01748
    
    Mg:    is your uid and 
    bmecjm-836936a57f2b488b0b5848ef9ab01748:  is your token

> `/auth/users/reset_password_confirm/` (POST): To confirm password reset.


    {
	    "uid": "Mg",
	    "token": "bmecjm-836936a57f2b488b0b5848ef9ab01748"
    }


# Authentication

This project uses JWTAuthentication for authentication.

To authenticate a user and obtain a JWT token, send a POST request to the > `/auth/jwt/create/` endpoint with the user's credentials. 

The response will contain an access token and a refresh token. 

To access protected endpoints, include the access token in the request header with the prefix "JWT"(in Postman). 

For example: 

    Authorization: JWT eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTY4MTY1OTYxNiwianRpIjoiMGE1NWQ3NjY3NTQ5NDE2N2IxYjQ4YWExMmQ3MDYxZDUiLCJ1c2VyX2lkIjoyfQ.PLFx-W_Z0vycWtoqlZd1KaF7vs5qCW1qkdgat92s07Q


Note: In the request header, the prefix for JWT tokens is "JWT" instead of "Token".
You Need this to access the following endpoints.

# Endpoints that require authentication

> `/api/verify-business/` (POST): For Document Verification. some of the Feilds are FileFeilds.

> `/api/balance/` (GET): To check balance.

> `/api/bank-detail/` (POST): To create new bank detail.


    {
		"account_name": "baabbii alex",
		"account_number": "700306178327",
		"bank_name": 3
    }

> `/api/bank-detail/` (GET): To View all you bank details.


> `/api/bank-detail/3/` (DELETE): To Delete selected  bank details with their ids.

> `/api/transfer/` (POST): To transfer money to bank detail.


    {
	"amount": "20.00",
	"bank_detail_id": 5
    }

> `/api/transactions/` (GET): To View all transactions.

> `/api/transactions/18/` (GET): To View a single transactions.


# Admin Site

admin site for managing users and transactions. To access the admin site, log in to the Django admin at http://localhost:8000/admin/ with your superuser credentials.


# Author

>Yohanes Alemu - [GitHub](https://github.com/baabbii69)   | [Telegram](https://t.me/Jinx_69) 
