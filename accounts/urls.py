from django.urls import path
from .views import *

urlpatterns = [
    path('verify-business/', VerifyBusinessView.as_view(), name='verify_business'),
    path('balance/', CheckBalanceView.as_view(), name='check_balance'),
    path('bank-detail/', BankDetailView.as_view(), name='bank_detail'),
    path('bank-detail/<int:pk>/', BankDetailView.as_view(), name='bank_detail'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('transactions/<int:pk>/', TransactionList.as_view(), name='transaction_list'),
]
