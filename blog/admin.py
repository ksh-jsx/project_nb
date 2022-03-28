from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Post,Tags,Comment,CustomUser,Items,Blog,Like
from .forms import (CustomUserCreationForm, CustomUserChangeForm)

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Tags)
admin.site.register(Items)
admin.site.register(Blog)
admin.site.register(Like)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
     
    # add page
    add_form = CustomUserCreationForm
    add_fieldsets = (
        
        ('ID & PASSWORD', {'fields': ('username', 'password1', 'password2')}),
        ('NAME', {'fields': ('name')}),
        ('PERSONAL INFO', {'fields': ('gender', 'job','email address')}),
        ('PERMISSIONS', {'fields': ('is_active', 'is_staff', 'is_superuser')})
    )
     
    # change page
    form = CustomUserChangeForm
    fieldsets = (
        
        ('ID & PASSWORD', {'fields': ('username', 'password')}),
        ('NAME & EMAIL', {'fields': ('name','email')}),
        ('PERSONAL INFO', {'fields': ('gender', 'job',)}),
        ('PERMISSIONS', {'fields': ('is_active', 'is_staff', 'is_superuser','active')}),
    )
     
    # list page
    list_display = ['username','name', 'email', 'gender', 'job','created_at','active']
 
 
admin.site.register(CustomUser, CustomUserAdmin)

