
from django.urls import path
from .views import CustomUserCreate, BlacklistTokenUpdateView, usersLestView , FollowCreateView ,LoginView , userView , Logout
from rest_framework.routers import DefaultRouter
from .views import LoginUserView, UserDataView

app_name = 'users'

router = DefaultRouter()
urlpatterns = [
    path('create', CustomUserCreate.as_view(), name="create_user"),
    path('Login', LoginView.as_view(), name="Login"),
    path('userView', userView.as_view(), name="userView"),
    path('Logout', Logout.as_view(), name="Logout"),
    
    path('login2/', LoginUserView.as_view(), name='login'),
    path('UserData/', UserDataView.as_view(), name='UserDataView'),
    


    
    
    path('logout/blacklist/', BlacklistTokenUpdateView.as_view(),name='blacklist')

]
router.register('List', usersLestView, basename='userView')
router.register('Follow', FollowCreateView, basename='FollowCreateView')

# urlpatterns = router.urls
urlpatterns=urlpatterns+router.urls



