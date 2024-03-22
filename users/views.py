from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from .models import User
from .serializers import UserSerializer, FollowUserSerializer, UserProfileSerializer, UserProfileUpdateSerializer
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated



# Create your views here.
class UserListAPIView(APIView):
    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Get a list of all users.",
        responses={
            200: UserSerializer(many=True),
            401: "Unauthorized. User not authenticated.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Search for users by username.",
        manual_parameters=[
            openapi.Parameter('search_query', openapi.IN_QUERY, description="Search query string for username.",
                              type=openapi.TYPE_STRING),
        ],
        responses={
            200: UserSerializer(many=True),
            400: "Bad request. Invalid input data.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def post(self, request):
        search_query = request.data.get('search_query', None)
        if search_query:
            users = User.objects.filter(username__icontains=search_query)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)



class MyPageAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Get current user's profile data including recipes which was posted.",
        responses={200: UserProfileSerializer()},
    )

    def get(self, request, *args, **kwargs):
        try:
            profile = User.objects.get(id=request.user.id)
        except User.DoesNotExist:
            return Response({'data': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        profile_info = UserProfileSerializer(profile)
        content = {"Profile Info": profile_info.data}
        return Response(content, status=status.HTTP_200_OK)
class MyPageUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated,]

    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Update current user's profile data.",
        responses={200: UserProfileUpdateSerializer()},
    )

    def put(self, request, *args, **kwargs):
        try:
            user = request.user
            serializer = UserProfileUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'data': 'User not found'}, status=status.HTTP_404_NOT_FOUND)





class FollowUserAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Follow or unfollow a user.",
        responses={
            200: "User followed or unfollowed successfully.",
            400: "Bad request. Invalid input data.",
            404: "User not found.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def post(self, request, *args, **kwargs):
        try:
            following_user = User.objects.all().get(id=kwargs['user_id'])
        except:
            return Response({'data': 'Page not found'}, status=status.HTTP_404_NOT_FOUND)

        follower = request.user

        if follower == following_user:
            return Response({"message": "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if follower in following_user.follow.all():
            return Response({"message": "You are already following this user"}, status=status.HTTP_400_BAD_REQUEST)

        following_user.follow.add(follower)
        follower.following.add(following_user)

        return Response({"message": "You are now following this user"}, status=status.HTTP_201_CREATED)


class UnfollowUserAPIView(APIView):
    @swagger_auto_schema(
        tags=['Users'],
        operation_description="Unfollow a user.",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user to unfollow.",
                              type=openapi.TYPE_INTEGER),
        ],
        responses={
            200: "Successfully unfollowed user.",
            400: "Bad request. Invalid input data.",
            404: "User not found.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def post(self, request, user_id):
        # получение пользователя от которого нужно отписаться
        followed_user = User.objects.get(id=user_id)
        # Получаем текущего пользователя
        current_user = request.user
        # Удаляем followed user из список подписок текущего пользователя
        current_user.following.remove(followed_user)
        return Response("Successfully unfollowed user", status=status.HTTP_200_OK)


