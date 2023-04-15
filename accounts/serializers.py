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


class BankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetail
        fields = ['id', 'account_name', 'account_number', 'bank_name']

class TransactionSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    bank_id = serializers.IntegerField()
    bank = BankDetailSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'user', 'amount', 'bank', 'timestamp']

    # def create(self, validated_data):
    #     user = self.context['request'].user
    #     bank = BankDetail.objects.get(id=validated_data['bank_id'])
    #     transaction = Transaction.objects.create(
    #         user=user,
    #         bank=bank,
    #         amount=validated_data['amount']
    #     )
    #     return {
    #         'transaction_id': transaction.id,
    #         'user': user.username,
    #         'amount': validated_data['amount'],
    #         'bank': BankDetailSerializer(bank).data,
    #         'timestamp': transaction.timestamp
    #     }



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