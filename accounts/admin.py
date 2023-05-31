from django.contrib import admin
from django.contrib.auth.models import Group

from .models import *
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    fields = ['id', 'email', 'first_name', 'last_name', 'business_name', 'is_staff', 'is_superuser', 'is_active']
    list_display = ('email', 'id')
    list_filter = ('business_name', 'email')


class TransactionAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)
    list_display = ('id', 'user')
    list_filter = ('user', 'timestamp')


class WalletAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance')
    list_filter = ('user',)


class VerifyDocumentAdmin(admin.ModelAdmin):
    list_display = ('legal_BN', 'user')
    list_filter = ('user', 'legal_BN')


class ConnectedBankssAdmin(admin.ModelAdmin):
    list_display = ('name', 'bank_id', 'account_number')
    list_filter = ('name', 'account_number')


admin.site.site_header = 'QuickPay Business Admin Panel'
admin.site.register(User, UserAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(VerifyDocument, VerifyDocumentAdmin)
admin.site.register(ConnectedBankss, ConnectedBankssAdmin)
admin.site.unregister(Group)
admin.site.register((Industry, Incorporation, States, DedicatedPerson))
