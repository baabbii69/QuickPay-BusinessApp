from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'business_name')


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)


class BanksConnectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedBankss
        fields = ['id', 'bank_id', 'name', 'account_number']


class TransactionSerializer(serializers.ModelSerializer):
    bank = serializers.CharField(source='bank.name')
    timestamp = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'bank', 'description', 'timestamp']


class StatesSerializer(serializers.ModelSerializer):
    class Meta:
        model = States
        fields = ['id', 'state_name']


class IndustrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Industry
        fields = ['id', 'industry_name']
        read_only_fields = ['id']


class IncorporationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Incorporation
        fields = ['id', 'incorp_name']
        read_only_fields = ['id']


class VerifyBusinessSerializer(serializers.ModelSerializer):
    industrys = IndustrySerializer()
    incorp_type = IncorporationSerializer()

    class Meta:
        model = VerifyDocument
        fields = ['id', 'business_type', 'industrys', 'category', 'staff_size', 'trans_volume', 'legal_BN',
                  'tin_numbers', 'vat_check', 'business_reg_num', 'incorp_type', 'trade_license',
                  'tin_certificate', 'memorandum', 'business_contact', 'proof_address', 'states',
                  'kifle_ketema', 'woreda', 'kebele', 'house_number', 'frendly_BN', 'business_phone', 'business_email']
        read_only_fields = ['id']
