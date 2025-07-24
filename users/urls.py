from django.urls import path
from .views import RequestAuthCodeView

urlpatterns = [
    path('request-code/', RequestAuthCodeView.as_view(), name='request-code'),
]