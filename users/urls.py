from django.urls import path
from .views import RequestAuthCodeView, VerifyCodeView

urlpatterns = [
    path('request-code/', RequestAuthCodeView.as_view(), name='request-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
]