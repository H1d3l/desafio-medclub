from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from .models import *
from .serializers import *

# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['GET'])
    def get_profile_by_user_id(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
            profile = Profile.objects.get(user=user)
            serializer = ProfileSerializer(profile, context={'request': request})
            return Response(serializer.data, status= status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)



class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    authentication_classes = [BasicAuthentication]
    permission_classes = [IsAuthenticated]


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def list(self, request, *args, **kwargs):
        orders = Order.objects.all()

        orders_info = []
        for order in orders:
            order_info = {
                'id': order.id,
                'user': order.user.id,
                'date_ordered': order.date_ordered,
                'items': [item.name for item in order.items.all()]
            }
            orders_info.append(order_info)

        return Response(orders_info, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()

            response_data = {
                "id": order.id,
                "date_ordered": order.date_ordered,
                "user": order.user.id,
                "items": [item.name for item in order.items.all()]
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)

            response_data = {
                "id": order.id,
                "date_ordered": order.date_ordered,
                "user": order.user.id,
                "items": [item.name for item in order.items.all()]
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    def update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = self.get_serializer(order, data=request.data)
            if serializer.is_valid():
                serializer.save()

                response_data = {
                    "id": order.id,
                    "date_ordered": order.date_ordered,
                    "user": order.user.id,
                    "items": [item.name for item in order.items.all()]
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
            serializer = self.get_serializer(order, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                response_data = {
                    "id": order.id,
                    "date_ordered": order.date_ordered,
                    "user": order.user.id,
                    "items": [item.name for item in order.items.all()]
                }
                return Response(response_data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Order.DoesNotExist:
            return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=True, methods=['GET'])
    def get_order_by_profile_id(self, request, pk=None):
        try:
            profile = Profile.objects.get(pk=pk)
            order = Order.objects.filter(user=profile)
            if order:
                serializer = OrderSerializer(order, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                Response({"detail": "There is no request for this user."}, status=status.HTTP_404_NOT_FOUND)
        except Profile.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)