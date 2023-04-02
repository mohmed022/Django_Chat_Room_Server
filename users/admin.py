from django.contrib import admin
from users.models import NewUser
from django.contrib.auth.admin import UserAdmin
from django.forms import TextInput, Textarea, CharField
from django import forms
from django.db import models


class UserAdminConfig(UserAdmin):
    model = NewUser
    search_fields = ('id','email', 'user_name', 'first_name',)
    list_filter = ('id','email', 'user_name', 'first_name', 'is_active', 'is_staff' , "is_Assistant" , "is_online" , "is_activeChat" ,"university","sections")
    ordering = ('-start_date',)
    list_display = ('id','email', 'user_name', 'first_name',
                    'is_active', 'is_staff','is_Assistant' , "is_online" , "is_activeChat" ,"university","sections")
    fieldsets = (
        (None, {'fields': ('email', 'user_name', 'first_name',)}),
        ('Permissions', {'fields': ('is_staff', 'is_active' , 'is_Assistant' , "is_online" , "is_activeChat" ,"university","sections")}),
        ('Personal', {'fields': ('about',)}),
    )
    formfield_overrides = {
        models.TextField: {'widget': Textarea(attrs={'rows': 20, 'cols': 60})},
    }
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'user_name', 'first_name', 'password1', 'password2', 'is_active', 'is_staff','is_Assistant' , "is_online" , "is_activeChat"  ,"university","sections")}
         ),
    )


admin.site.register(NewUser, UserAdminConfig)

