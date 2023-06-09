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
    path('user/', UserListView.as_view(), name='users'),
    path('u/', VerifyDocumentAPIView.as_view(), name='tests'),
    path('auth/users/activation/<str:uidb64>/<str:token>/', account_activation, name='useraccount-activation'),
    path('activation/success/', activation_success, name='activation_success'),
    path('activation/error/', activation_error, name='activation_error'),
    path('industry/', IndustryView.as_view(), name='industry'),
    path('state/', StatesView.as_view(), name='state'),
    path('incorporation/', IncorporationView.as_view(), name='incorporation'),

    # path('sent-to-user/', UtilityView.as_view(), name='utility_to_user'),
    # path('utility-pay/', UtilityPayView.as_view(), name='utility_pay'),
]
