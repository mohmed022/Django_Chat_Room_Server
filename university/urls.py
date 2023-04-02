


from django.urls import path
from .views import PaymentConfirmationView ,PhoneTrnsView ,TasksView, PackageView,  university_ModelsView , universityPhotoArryView , universityVideoArryView , sections_ModelsView , sectionsPhotoArryView , sectionsVideoArryView ,universityDescriptionView , FormAplctionUserView
from rest_framework.routers import DefaultRouter

app_name = 'university'

router = DefaultRouter()
urlpatterns = [
]
router.register('Listuniversity', university_ModelsView, basename='Listuniversity')
router.register('ListDescription', universityDescriptionView, basename='ListDescription')
router.register('Listuniversityphoto', universityPhotoArryView, basename='Listuniversityphoto')
router.register('Listuniversityvideo', universityVideoArryView, basename='Listuniversityvideo')
router.register('FormAplctionUser', FormAplctionUserView, basename='FormAplctionUser')
router.register('Package', PackageView, basename='Package')
router.register('Tasks', TasksView, basename='Tasks')
router.register('PhoneTrns', PhoneTrnsView, basename='PhoneTrns')
router.register('PaymentConfirmation', PaymentConfirmationView, basename='PaymentConfirmation')




router.register('Listsections', sections_ModelsView, basename='Listsections')
router.register('Listsectionsphoto', sectionsPhotoArryView, basename='Listsectionsphoto')
router.register('Listsectionsvideo', sectionsVideoArryView, basename='Listsectionsvideo')








# urlpatterns = router.urls
urlpatterns=urlpatterns+router.urls



