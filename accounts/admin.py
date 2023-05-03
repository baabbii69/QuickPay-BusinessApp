from django.contrib import admin
from .models import *


admin.site.register((Industry, Incorporation, States, DedicatedPerson, VerifyDocument, Wallet, BankDetail, Transaction, ConnectedBankss))
