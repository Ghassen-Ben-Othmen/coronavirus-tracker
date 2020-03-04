from django.urls import path
from .views import LoginAPIView, RegisterAPIView, LogoutAPIView


urlpatterns = [
    path('login/', LoginAPIView.as_view(), name='login-user'),
    path('register/', RegisterAPIView.as_view(), name='register-user'),
    path('logout/', LogoutAPIView.as_view(), name='logout-user')
]
