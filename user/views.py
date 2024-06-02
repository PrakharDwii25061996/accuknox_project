""" user/views.py """
from django_ratelimit.decorators import ratelimit

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from django.shortcuts import render, HttpResponse, get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator

from .models import CustomUser, FriendRequest
from .serializers import (
    CustomUserSerializer,
    UserAuthTokenSerializer,
    FriendRequestSerializer,
    FriendRequestUpdateSerializer
)
from .pagination import CustomPagination


class CustomUserAPIView(generics.CreateAPIView):
    """
    API through which any user can register
    """

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomLoginAPIView(ObtainAuthToken):
    """
    API through which registered user can login
    """

    serializer_class = UserAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = UserAuthTokenSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data["user"]
            token, created = Token.objects.get_or_create(user=user)
            response_data = {"email": user.email, "token": token.key}
            return Response(response_data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserListAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        users = self.get_queryset()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class SearchUserAPIView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_user_by_name(self):
        search_word = self.request.query_params.get("word")
        users = CustomUser.objects.filter(
            Q(full_name__icontains=search_word) | Q(email__icontains=search_word)
        )
        return users

    def get(self, request, *args, **kwargs):
        users = self.get_user_by_name()
        # serializer = CustomUserSerializer(users, many=True)
        page = self.paginate_queryset(users)

        if page is not None:
            serializer = CustomUserSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return Response(page, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestAPIView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_pending_friend_request(self):
        pending_friend_request = FriendRequest.objects.filter(
            from_user=self.request.user, is_accepted=False, is_rejected=False
        )
        return pending_friend_request

    @method_decorator(ratelimit(key='user', rate='3/m'))
    def post(self, request, *args, **kwargs):
        """
        Sends a friend request to a user.
        """
        serializer = FriendRequestSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, *args, **kwargs):
        """
        List of user having pending friend request
        """
        friend_requests = self.get_pending_friend_request()
        serializer = FriendRequestSerializer(friend_requests, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestAcceptedAPIView(generics.ListCreateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_accepted_friend_request(self):
        """
        get accepted friend request list of user.
        """
        accepted_friend_request = FriendRequest.objects.filter(
            from_user=self.request.user, is_accepted=True, is_rejected=False
        )
        return accepted_friend_request

    def get(self, request, *args, **kwargs):
        """
        List of user having pending friend request
        """
        accepted_friend_request = self.get_accepted_friend_request()
        serializer = FriendRequestSerializer(accepted_friend_request, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class FriendRequestAcceptRejectAPIView(generics.UpdateAPIView):
    queryset = FriendRequest.objects.all()
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self, friend_request_id):
        try:
            friend_request = FriendRequest.objects.get(id=friend_request_id)
        except FriendRequest.Vehicle.DoesNotExist:
            print(e)
        return friend_request

    def patch(self, request, *args, **kwargs):
        """
        Friend request accepted or rejected.
        """
        friend_request = self.get_object(kwargs.get('id'))
        serializer = FriendRequestUpdateSerializer(instance=friend_request, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
