from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializers import VerifyBusinessSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

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