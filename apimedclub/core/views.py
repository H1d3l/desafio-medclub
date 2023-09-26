from django.contrib.auth.models import User
from .models import *
from .serializers import *
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import  IsAuthenticated
from django.shortcuts import get_object_or_404


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
        user = get_object_or_404(User, pk=pk)

        profile = Profile.objects.get(user = user)
        serializer = ProfileSerializer(profile,context={'request': request})
        return Response(serializer.data)




