from django.urls import path
from .views import *

urlpatterns = [
    path('verify-business/', VerifyBusinessView.as_view(), name='verify_business'),
    path('balance/', CheckBalanceView.as_view(), name='check_balance'),
    path('connect-bank/', BankConnectView.as_view(), name='connect_bank'),
    path('bank-detail/', ListBankConnectView.as_view(), name='bank_detail'),
    path('bank-detail/<int:pk>/', ListBankConnectView.as_view(), name='bank_detail_1'),
    path('withdraw/', WithdrawToBankView.as_view(), name='withdraw_to_bank'),
    path('transactions/', TransactionList.as_view(), name='transaction_list'),
    path('banks/', GetBankListView.as_view(), name='banks'),
    path('transactions/<int:pk>/', TransactionList.as_view(), name='transaction_list'),
    path('deposit-to-wallet/', DepositToWalletView.as_view(), name='deposit_to_wallet'),
    path('user/', UserListView.as_view(), name='users')
]
