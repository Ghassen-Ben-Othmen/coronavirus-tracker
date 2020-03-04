from django.urls import path
from .views import DataAPIView

urlpatterns = [
    path('', DataAPIView.as_view(), name='data')
]
