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
        model = Balance
        fields = ('balance',)
class BankSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'bank_name']
        read_only_fields = ['id']

class BankDetailSerializer(serializers.ModelSerializer):
    bank_name = serializers.PrimaryKeyRelatedField(queryset=Bank.objects.all())

    class Meta:
        model = BankDetail
        fields = ['id', 'account_name', 'account_number', 'bank_name']

    def validate_bank_name(self, value):
        user = self.context['request'].user
        if BankDetail.objects.filter(user=user, bank_name=value).exists():
            raise serializers.ValidationError('Bank detail with this bank name already exists.')
        return value

class TransactionSerializer(serializers.ModelSerializer):
    bank_detail = BankDetailSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'bank', 'timestamp', 'bank_detail']

    def create(self, validated_data):
        bank_detail = validated_data.pop('bank_detail')
        transaction = Transaction.objects.create(bank_detail=bank_detail, **validated_data)
        return transaction




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