from django.urls import path
from .views import VerifyBusinessView

urlpatterns = [
    path('verify-business/', VerifyBusinessView.as_view(), name='verify_business'),
]
