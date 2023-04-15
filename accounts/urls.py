from django.urls import path
from .views import *

urlpatterns = [
    path('verify-business/', VerifyBusinessView.as_view(), name='verify_business'),
    path('balance/', CheckBalanceView.as_view(), name='check_balance'),
]
