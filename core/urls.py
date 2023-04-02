# start static
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import *  # NOQA
# End static

from django.contrib import admin
from django.urls import path, include 
# from rest_framework.schemas import get_schema_view
# from rest_framework.documentation import include_docs_urls
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from django.conf import settings
from django.conf.urls.static import static





urlpatterns = [
    # API Token Management
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Project URLs
    path('admin/', admin.site.urls),
    # User Management
    path('api/user/', include('users.urls', namespace='users')),
    path('api/', include('university.urls')),
    path('', include('chat.urls')),
    path('api/', include('chat2.urls')),
    path('api2/', include('chat3.urls')),
    # path('api-auth/', include('rest_framework.urls')),

    
    


]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)









