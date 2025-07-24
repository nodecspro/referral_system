from django.urls import path
from .views import RequestAuthCodeView, VerifyCodeView, UserProfileView

urlpatterns = [
    path('request-code/', RequestAuthCodeView.as_view(), name='request-code'),
    path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]