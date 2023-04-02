from django.urls import path
from Profile.views import ProfileViewSet
from todo.views import AdminLessonsDetail, Createlesson, DeleteLessons, EditLessons, Subjects_MView ,LessonsView,LessonsListSerializer
from users.views import usersLestView
from Subjects.views import SubjectsListView ,SubjectsCreateView ,LissonsListView , Lessons_SubjectSerializer
from rest_framework.routers import DefaultRouter

app_name = 'api'

router = DefaultRouter()



urlpatterns = [
# urlpatterns = router.urls
path('Lesson/create/', Createlesson.as_view(), name='Createlesson'),
    path('Lesson/edit/postdetail/<int:pk>/', AdminLessonsDetail.as_view(), name='admindetailpost'),
    path('Lesson/edit/<int:pk>/', EditLessons.as_view(), name='editpost'),
    path('Lesson/delete/<int:pk>/', DeleteLessons.as_view(), name='deletepost'),

]

# router.register(r'users', UserViewSet,basename='users')


router.register(r'LissonsListView', LissonsListView, basename='LissonsListView')
router.register(r'Lessons_SubjectSerializer', Lessons_SubjectSerializer, basename='Lessons_SubjectSerializer')

router.register(r'usersLestView', usersLestView, basename='usersLestView')
router.register(r'ProfileViewSet', ProfileViewSet, basename='ProfileViewSet')
router.register(r'Subjects_MView', Subjects_MView, basename='Subjects_MView')
router.register(r'LessonsView', LessonsView, basename='LessonsView')
router.register(r'LessonsListSerializer', LessonsListSerializer, basename='LessonsListSerializer')

urlpatterns=urlpatterns+router.urls

