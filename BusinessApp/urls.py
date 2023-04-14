
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('api/', include('accounts.urls')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
