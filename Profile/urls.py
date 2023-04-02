from .views import ProfileViewSet
from rest_framework.routers import DefaultRouter

app_name = 'Profile'

router = DefaultRouter()
router.register('ProfileViewSet', ProfileViewSet, basename='ProfileViewSet')
urlpatterns = router.urls

