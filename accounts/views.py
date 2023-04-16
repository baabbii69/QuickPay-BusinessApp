from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import *
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

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
        user_balance = Balance.objects.get(user=request.user)
        serializer = BalanceSerializer(user_balance)
        return Response(serializer.data)


class BankDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        bank_details = BankDetail.objects.filter(user=request.user)
        serializer = BankDetailSerializer(bank_details, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = BankDetailSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def put(self, request, pk, format=None):
    #     try:
    #         bank_detail = BankDetail.objects.get(pk=pk, user=request.user)
    #     except BankDetail.DoesNotExist:
    #         return Response(status=status.HTTP_404_NOT_FOUND)

    #     serializer = BankDetailSerializer(bank_detail, data=request.data, context={'request': request})
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        try:
            bank_detail = BankDetail.objects.get(pk=pk, user=request.user)
        except BankDetail.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        bank_detail.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = TransactionSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data.get('amount')
            bank_detail_id = serializer.validated_data.get('bank_detail_id')
            bank = None
            try:
                bank = BankDetail.objects.get(id=bank_detail_id)
            except BankDetail.DoesNotExist:
                return Response({'error': 'Invalid bank_detail_id'}, status=status.HTTP_400_BAD_REQUEST)
            user = request.user

            balance = None
            try:
                balance = Balance.objects.get(user=user)
            except Balance.DoesNotExist:
                return Response({'error': 'Balance does not exist'}, status=status.HTTP_400_BAD_REQUEST)

            if balance.balance >= amount:
                balance.balance -= amount
                balance.save()

                transaction = Transaction(
                    user=user,
                    amount=amount,
                    bank=bank
                )
                transaction.save()
                transaction_serializer = TransactionSerializer(transaction)
                return Response({'message': 'Transaction successful.', 'transaction_id': transaction.id}, status=status.HTTP_201_CREATED)
            else:
                return Response({'error': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
