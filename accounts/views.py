import requests
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
import httpx
from asgiref.sync import sync_to_async
from django.http import JsonResponse

from .models import *


class VerifyBusinessView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = VerifyBusinessSerializer(data=request.data)
        if serializer.is_valid():
            if serializer.validated_data['business_type']:
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Business must be verified'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckBalanceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_balance = Wallet.objects.get(user=request.user)
        serializer = BalanceSerializer(user_balance)
        return Response(serializer.data)


class BankConnectView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        bank_id = request.data.get('bank_id')
        account_number = request.data.get('account_number')

        response = requests.get(f"http://localhost:1300/banks/{bank_id}/")
        if response.status_code != 200:
            return Response({'error': 'Invalid bank ID'}, status=status.HTTP_400_BAD_REQUEST)

        bank_data = response.json()

        bank = ConnectedBankss(
            bank_id=bank_data['id'],
            name=bank_data['name'],
        )

        response = requests.post(f"http://127.0.0.1:1200/banks/get-account",
                                 json={'account_number': account_number, 'bank_id': bank_id})

        if response.status_code == 200:
            bank.account_number = account_number
            bank.user = request.user
            bank.save()
            serializer = BanksConnectedSerializer(bank)

            return Response({'success': 'Bank account connected'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid account number'}, status=status.HTTP_400_BAD_REQUEST)


class ListBankConnectView(APIView):
    permission_classes = [IsAuthenticated]

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
            return Response({'success': 'Bank account disconnected'}, status=status.HTTP_200_OK)
        except ConnectedBankss.DoesNotExist:
            return Response({'error': 'Bank account not found'}, status=status.HTTP_404_NOT_FOUND)


class WithdrawToBankView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        bank_id = request.data.get('bank_id')
        bank = get_object_or_404(ConnectedBankss, pk=bank_id, user=request.user)
        balance = Wallet.objects.get(user=request.user)
        account_number = bank.account_number

        response = requests.post(
            f"http://localhost:1200/businesses/withdraw",
            json={"amount": amount, 'bank_id': bank_id, "account_number": account_number}
        )

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

                return Response({'success': 'Withdrawal successful', 'transaction': transaction_serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Insufficient funds'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Withdrawal Fail'}, status=status.HTTP_400_BAD_REQUEST)


# class DepositToWalletView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         amount = request.data.get('amount')
#         user_id = request.user.id
#         description = request.data.get('description')
#
#         response = requests.post(
#             f"http://localhost:1200/businesses/deposit",
#             json={"amount": amount, 'user_id': user_id}
#         )
#
#         if response.status_code == 200:
#             balance = Wallet.objects.get(user=request.user)
#             balance.balance += amount
#             balance.save()
#             transaction = Transaction.objects.create(
#                 user=request.user,
#                 amount=amount,
#                 description=description,
#             )
#             transaction_serializer = TransactionSerializer(transaction)
#
#             return Response({'success': 'Deposit successful', 'transaction': transaction_serializer.data}, status=status.HTTP_201_CREATED)
#         else:
#             return Response({'error': 'Deposit Fail'}, status=status.HTTP_400_BAD_REQUEST)
#

class TransactionList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None, format=None):
        if pk:
            transactions = Transaction.objects.filter(pk=pk, user=request.user)
            if not transactions:
                return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            transactions = Transaction.objects.filter(user=request.user)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
