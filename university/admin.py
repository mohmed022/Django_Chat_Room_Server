from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(university_Models)
admin.site.register(universityDescription_Models)
admin.site.register(universityPhotoArry_Models)
admin.site.register(sections_Models)
admin.site.register(sectionsPhotoArry_Models)

admin.site.register(FormAplctionUser_Models)
admin.site.register(Package_Models)
admin.site.register(Tasks_Models)
admin.site.register(PhoneTrns_Models)
admin.site.register(PaymentConfirmation_Models)



