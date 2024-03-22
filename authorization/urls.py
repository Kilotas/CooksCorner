from django.urls import path
from .views import RegisterEmailView, VerifyEmail, RegisterPersonalInfoView, LoginAPIView
from rest_framework_simplejwt.views import (
    TokenRefreshView
)
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions
from dishes.views import RecipeCreateAPIView, RecipeListAPIView, RecipeDetailAPIView, RecipeCategoryAPIView, RecipeSearchAPIView
from users.views import UserListAPIView, FollowUserAPIView, UnfollowUserAPIView, MyPageAPIView, MyPageUpdateAPIView


schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('register/email/', RegisterEmailView.as_view(), name='email-verification'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('register/personal-info/', RegisterPersonalInfoView.as_view(), name='register-personal-info'),
    path('recipes/', RecipeCreateAPIView.as_view(), name='recipe-create'),
    path('main/', RecipeListAPIView.as_view(), name='main-page'),
    path('recipes/<int:pk>/', RecipeDetailAPIView.as_view(), name='recipe-detail'),
    path('recipes/category/<str:category>', RecipeCategoryAPIView.as_view(), name='recipe_category'),
    path('recipes/search/', RecipeSearchAPIView.as_view(), name='recipe_search'),
    path('users/', UserListAPIView.as_view(), name='user-list'),
    path('users/<int:user_id>/follow/', FollowUserAPIView.as_view(), name='follow_user'),
    path('users/<int:user_id>/unfollow/', UnfollowUserAPIView.as_view(), name='unfollow_user'),
    path('mypage/', MyPageAPIView.as_view(), name='mypage'),
    path('my-page/update', MyPageUpdateAPIView.as_view(), name='my-page-update'),
]



