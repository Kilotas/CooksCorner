from django.urls import path
from .views import RegisterEmailView, LoginAPIView

urlpatterns = [
    path('register/', RegisterEmailView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name="login"),
]
