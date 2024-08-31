from django.shortcuts import render

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Transaction
from .serializers import TransactionSerializer

class TransactionListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        data = Transaction.objects.filter(user=user)
        serializer = TransactionSerializer(data, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        data = request.data
        serializer = TransactionSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
