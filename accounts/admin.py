from django.contrib import admin
from .models import *
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ['id', 'email', 'first_name', 'last_name', 'business_name', 'is_staff', 'is_superuser', 'is_active']


admin.site.register(User, UserAdmin)

admin.site.register((Industry, Incorporation, States, DedicatedPerson, VerifyDocument, Wallet, BankDetail, Transaction, ConnectedBankss))
