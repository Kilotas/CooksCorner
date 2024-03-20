from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Recipe, Like
from .serializers import RecipeSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class RecipeCreateAPIView(APIView):
    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Endpoint for creating a new recipe.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'recipe_name': openapi.Schema(type=openapi.TYPE_STRING),
                'category': openapi.Schema(type=openapi.TYPE_INTEGER),
                'cooking_time': openapi.Schema(type=openapi.TYPE_STRING),
                'difficulty': openapi.Schema(type=openapi.TYPE_STRING),
                'description': openapi.Schema(type=openapi.TYPE_STRING),
                'ingredients': openapi.Schema(type=openapi.TYPE_ARRAY, items=openapi.Schema(type=openapi.TYPE_INTEGER)),
                'image': openapi.Schema(type=openapi.TYPE_STRING, format=openapi.FORMAT_BINARY),
            },
            required=['recipe_name', 'category', 'cooking_time', 'difficulty', 'description', 'ingredients']
        ),
        responses={
            201: "Successful creation. Returns the created recipe.",
            400: "Bad request. Invalid input.",
            401: "Unauthorized. User not authenticated.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def post(self, request):
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RecipeListAPIView(APIView):
    permission_classes = [IsAuthenticated, ]

    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Endpoint for retrieving a list of all recipes.",
        responses={
            200: "Successful retrieval. Returns a list of recipes.",
            401: "Unauthorized. User not authenticated.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request):
        recipes = Recipe.objects.all()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class RecipeDetailAPIView(APIView):
    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Endpoint for retrieving details of a specific recipe.",
        responses={
            200: "Successful retrieval. Returns the details of the recipe.",
            404: "Not found. Recipe with the specified primary key does not exist.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get(self, request, pk):
        try:
            recipe = Recipe.objects.get(pk=pk)
            serializer = RecipeSerializer(recipe)
            return Response(serializer.data)
        except Recipe.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        

class RecipeCategoryAPIView(APIView):
    permission_classes = [IsAuthenticated,]
    @swagger_auto_schema(
        tags=['Recipes'],
        operation_description="Endpoint for retrieving a list of recipes by category. 'BREAKFAST', 'DINNER', or 'LUNCH'.",
        manual_parameters=[
            openapi.Parameter('category', openapi.IN_QUERY, description="Filter recipes by category.", type=openapi.TYPE_STRING),
        ],
        responses={
            200: "Successful retrieval. Returns a list of recipes.",
            401: "Unauthorized. User not authenticated.",
            500: "Internal server error. Failed to process the request."
        }
    )
    def get_queryset(self):
        category = self.kwargs['category']
        return Recipe.objects.filter(category=category)

    def get(self, request, category):
        recipes = self.get_queryset()
        serializer = RecipeSerializer(recipes, many=True)
        return Response(serializer.data)








