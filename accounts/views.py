import decimal
import os
from djoser.conf import settings
from django.conf import settings


import requests
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from dotenv import load_dotenv
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_swagger import renderers
from rest_framework.schemas import SchemaGenerator
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from .models import *
from .serializers import *

from django.shortcuts import redirect
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings

load_dotenv()
User = get_user_model()


@csrf_exempt
def account_activation(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()

        # Send confirmation email
        current_site = get_current_site(request)
        mail_subject = 'Activate your account'
        message = render_to_string('email/confirmation.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': token,
        })
        send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

        # Redirect to a success page or any other desired URL
        return redirect('activation_success')
    else:
        # Redirect to an error page or any other desired URL
        return redirect('activation_error')


def activation_success(request):
    return HttpResponse("Activation Successful!")


def activation_error(request):
    return HttpResponse("Activation Error!")


class VerifyBusinessView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=VerifyBusinessSerializer,
        responses={200:VerifyBusinessSerializer(many=True)},
        operation_description="Verify a business",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def post(self, request, format=None):
        serializer = VerifyBusinessSerializer(data=request.data)
        user = request.user
        if serializer.is_valid():
            if serializer.validated_data['business_type']:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'Business must be verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IndustryView(APIView):
    def get(self, request):
        industries = Industry.objects.all()
        serializer = IndustrySerializer(industries, many=True)
        return Response(serializer.data)


class StatesView(APIView):
    def get(self, request):
        states = States.objects.all()
        serializer = StatesSerializer(states, many=True)
        return Response(serializer.data)


class IncorporationView(APIView):
    def get(self, request):
        incorporations = Incorporation.objects.all()
        serializer = IncorporationSerializer(incorporations, many=True)
        return Response(serializer.data)


class CheckBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200:BalanceSerializer(many=True)},
        operation_description="Check user balance",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def get(self, request):
        user_balance = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(user_balance)
        return Response(serializer.data)


class GetBankListView(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        response = requests.post(f"{os.getenv('SC_BASE_URL')}/banks/get-banks/")
        bank_list = response.json()
        return Response(bank_list)


class BankConnectView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=BanksConnectedSerializer,
        responses={200:BanksConnectedSerializer(many=True)},
        operation_description="Connect a bank account",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def post(self, request):
        bank_id = request.data.get('bank_id')
        account_number = request.data.get('account_number')
        user_id = request.user.id

        if ConnectedBankss.objects.filter(user_id=user_id, bank_id=bank_id, account_number=account_number).exists():
            return Response({'error':'Bank account already connected'}, status=status.HTTP_400_BAD_REQUEST)
        if ConnectedBankss.objects.filter(user_id=user_id, bank_id=bank_id).exists():
            return Response({'error':'Bank already connected'}, status=status.HTTP_400_BAD_REQUEST)

        response = requests.post(f"{os.getenv('SC_BASE_URL')}/banks/get-banks/")
        bank_list = response.json()
        print(bank_list)

        selected_bank = None
        for cs in bank_list:
            if cs['id'] == bank_id:
                selected_bank = cs
                break

        print(selected_bank)

        if response.status_code != 200:
            return Response({'error':'Invalid bank ID'}, status=status.HTTP_400_BAD_REQUEST)

        bank = ConnectedBankss(
            bank_id=selected_bank['id'],
            name=selected_bank['name'],
        )

        response = requests.post(f"{os.getenv('SC_BASE_URL')}/banks/get-account",
                                 json={'account_number':account_number, 'bank_id':bank_id})

        if response.status_code == 200:
            bank.account_number = account_number
            bank.user = request.user
            bank.save()
            serializer = BanksConnectedSerializer(bank)

            return Response({'success':'Bank account connected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error':'Invalid account number'}, status=status.HTTP_400_BAD_REQUEST)


class ListBankConnectView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200:BanksConnectedSerializer(many=True)},
        operation_description="List all connected bank accounts",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def get(self, request, pk=None, format=None):
        user_id = request.user.id
        if pk:
            connected_banks = ConnectedBankss.objects.filter(pk=pk, user_id=user_id)
            if not connected_banks:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            connected_banks = ConnectedBankss.objects.filter(user_id=user_id)

        serializer = BanksConnectedSerializer(connected_banks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, pk):
        user_id = request.user.id
        try:
            bank = ConnectedBankss.objects.get(pk=pk, user_id=user_id)
            bank.delete()
            return Response({'success':'Bank account disconnected'}, status=status.HTTP_200_OK)
        except ConnectedBankss.DoesNotExist:
            return Response({'error':'Bank account not found'}, status=status.HTTP_404_NOT_FOUND)


class WithdrawToBankView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        request_body=WithdrawSerializer,
        responses={200:TransactionSerializer(many=True)},
        operation_description="Withdraw from wallet to bank account",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def post(self, request):
        amount = request.data.get('amount')
        bank_id = request.data.get('bank_id')
        bank = get_object_or_404(ConnectedBankss, pk=bank_id, user=request.user)
        balance = Wallet.objects.get(user=request.user)
        account_number = bank.account_number

        response = requests.post(
            f"{os.getenv('SC_BASE_URL')}/businesses/withdraw",
            json={"amount":amount, 'bank_id':bank_id, "account_number":account_number}
        )
        print(response.json())
        if response.status_code == 200:
            if balance.balance >= amount:
                balance.balance -= amount
                balance.save()
                transaction = Transaction.objects.create(
                    user=request.user,
                    amount=amount,
                    bank=bank,
                    description=response.json()['description'],
                )
                transaction_serializer = TransactionSerializer(transaction)

                return Response({'success':'Withdrawal successful', 'transaction':transaction_serializer.data},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({'error':'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error':'Withdrawal Fail'}, status=status.HTTP_400_BAD_REQUEST)


class UserListView(APIView):

    def get(self, request):
        users = get_user_model().objects.all()
        print(users)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


class DepositToWalletView(APIView):

    def post(self, request):
        amount = request.data.get('amount')
        user_id = request.data.get('business_id')
        description = request.data.get('description')
        print(request.data)
        balance = Wallet.objects.get(user=user_id)
        user = get_user_model().objects.get(id=user_id)
        balance.balance += decimal.Decimal(amount)
        balance.save()
        transaction = Transaction.objects.create(
            user=user,
            amount=amount,
            description=description,
        )
        transaction_serializer = TransactionSerializer(transaction)

        return Response({'success':'Deposit successful', 'transaction':transaction_serializer.data},
                        status=status.HTTP_201_CREATED)


class TransactionList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        responses={200:TransactionSerializer(many=True)},
        operation_description="List all transactions",
        manual_parameters=[openapi.Parameter('Authorization', openapi.IN_HEADER, description="JWT <token>",
                                             type=openapi.TYPE_STRING, required=True)]
    )
    def get(self, request, pk=None, format=None):
        if pk:
            transactions = Transaction.objects.filter(pk=pk, user=request.user)
            if not transactions:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)


class UsersBusinessTypeView(APIView):
    def get(self, request):
        # usr = VerifyDocument.objects.filter(business_type=True)
        usr = VerifyDocument.objects.filter(business_type=True).values_list('user', flat=True)
        serializer = VerifyDocumentSerializer(usr, many=True)
        return Response(serializer.data)


class VerifyDocumentAPIView(APIView):
    def get(self, request):
        queryset = VerifyDocument.objects.filter(business_type=True).values_list('user', flat=True)
        serializer = VerifyDocumentSerializer(queryset, many=True)
        return Response(serializer.data)

# class CustomersAPIView(APIView):
#     def get(self, request):
#         response = requests.get(f"{os.getenv('SC_BASE_URL')}/users/")
#         if response.status_code == 200:
#             customer = Customer.objects.create(
#                 id=response.json()['id'],
#                 fname=response.json()['first_name'],
#                 lname=response.json()['last_name'],
#             )
#             customer_serializer = CustomerSerializer(customer)
#             return Response({'success': 'Customer created', 'customer': customer_serializer.data},
#                             status=status.HTTP_201_CREATED)
#
#
# class UtilityView(APIView):
#     def post(self, request):
#         amount = request.data.get('amount')
#         customer = request.data.get('customer')
#         bill_type = request.data.get('bill_type')
#         user_id = request.user.id
#         user = get_user_model().objects.get(user=user_id)
#
#         utility = Utility.objects.get(user=user_id)
#
#         response = requests.post(f"{os.getenv('SC_BASE_URL')}/utility/{customer}",
#                                  json={"amount": amount, "bill_type": bill_type,
#                                        "utility_name": utility.name, "utility_id": utility.user})
#         # utility = UtilityNormal.objects.create(
#         #     utility=utility,
#         #     amount=amount,
#         #     customer=customer,
#         #     bill_type=bill_type,
#         # )
#         # utility_serializer = UtilitySerializer(utility)
#         # return Response({'success': 'Utility created', 'utility': utility_serializer.data},
#         #                 status=status.HTTP_201_CREATED)
#         return Response(status=status.HTTP_200_OK)
#
#
# class UtilityPayView(APIView):
#     def post(self, request):
#         amount = request.data.get('amount')
#         customer = request.data.get('user')
#         user = request.data.get('utility_id')
#         bill_type = request.data.get('bill_type')
#         utility = Utility.objects.get(user=user)
#
#         balance = Wallet.objects.get(user=user)
#         balance.balance += decimal.Decimal(amount)
#         balance.save()
#
#         utility = UtilityNormal.objects.create(
#             utility=utility,
#             amount=amount,
#             customer=customer,
#             bill_type=bill_type,
#         )
#         utility_serializer = UtilitySerializer(utility)
#
#         return Response({'success': 'Utility Payed', 'utility': utility_serializer.data},
#                         status=status.HTTP_201_CREATED)
#

# class BillType(models.Model):
#     # fields for BillType
#
# class Utility(models.Model):
#     bill_types = models.ManyToManyField(BillType)
#     # fields for Utility
# $$$$$$$$$$$$$$$$$$$$$$$$$$$$4
# bill_type_instance = BillType.objects.get(id=bill_type_id)  # Retrieve the BillType instance
# utility_instance = Utility.objects.get(id=utility_id)  # Retrieve the Utility instance
#
# utility_instance.bill_types.add(bill_type_instance)  # Add the BillType instance to the ManyToManyField
