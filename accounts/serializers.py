from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()
from .models import *


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'password', 'business_name')


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email')


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ('balance',)


class BanksConnectedSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConnectedBankss
        fields = ['id', 'bank_id', 'name', 'account_number']


class TransactionSerializer(serializers.ModelSerializer):
    bank = serializers.CharField(source='bank.name', allow_null=True)
    timestamp = serializers.DateTimeField(format='%Y-%m-%dT%H:%M:%SZ')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'bank', 'description', 'timestamp']


class WithdrawSerializer(serializers.Serializer):
    class Meta:
        fields = ['amount', 'bank_id']


class TransactionnSerializer(serializers.ModelSerializer):
    timestamp = serializers.DateTimeField(format='%Y-%m-%d-%H:%M:%S')

    class Meta:
        model = Transaction
        fields = ['id', 'amount', 'description', 'timestamp']


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


# class UtilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Utility
#         fields = ['id', 'name', 'custemer', 'bill_amount', 'timestamp']
#         read_only_fields = ['id']


# class VerifyDocumentSerializer(serializers.ModelSerializer):
#     user = serializers.CharField(source='id', allow_null=True)
#
#     class Meta:
#         model = VerifyDocument
#         fields = '__all__'


class UsersAccountSerializer(serializers.ModelSerializer):
    verify_document = VerifyBusinessSerializer()

    class Meta:
        model = UserAccount
        fields = '__all__'


class VerifyDocumentSerializer(serializers.Serializer):
    user = serializers.UUIDField()

    def to_representation(self, instance):
        user_id = instance
        try:
            user = User.objects.get(id=user_id)
            return {'user': user.id}
        except User.DoesNotExist:
            return {'user': None}

# class CustomerSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Customer
#         fields = '__all__'
#
#
# class UtilitySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Utility
#         fields = '__all__'
# class BillTypeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = BillType
#         fields = '__all__'
#
#     def create(self, validated_data):
#         user_id = self.context['request'].user.id  # Assuming you have the current user in the request's context
#         utility_instance = Utility.objects.get(user_id=user_id)
#
#         bill_type = BillType.objects.create(**validated_data)
#         utility_instance.bill_types.add(bill_type)
#
#         return bill_type
