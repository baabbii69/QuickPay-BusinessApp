
from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="BusinessApp API",
        default_version='v1',
        description="This is the API for BusinessApp",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],

)


urlpatterns = [
    path('jet/', include('jet.urls', 'jet')),
    path('jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('', include([
        path('api/', include('accounts.urls')),
        path('', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
    ])),
]

# urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
