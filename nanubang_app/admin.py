from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from nanubang_app.models import User,Room_infos,Tags,Like,Connect,call_file,Complete_contract
from .forms import (UserCreationForm, UserChangeForm)

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = User
     
    # add page
    add_form = UserCreationForm
    add_fieldsets = (
        
        ('ID & PASSWORD', {'fields': ('username', 'password1', 'password2')}),
        ('NAME', {'fields': ('name')}),
        ('PERSONAL INFO', {'fields': ('gender','ciga', 'meet_path','email address','phone1','phone2','phone3')}),
        ('PERMISSIONS', {'fields': ('is_active', 'is_staff', 'is_superuser','payment','user_type','connector')})
    )
     
    # change page
    form = UserChangeForm
    fieldsets = (
        
        ('ID & PASSWORD', {'fields': ('username', 'password')}),
        ('NAME & EMAIL', {'fields': ('name','email')}),
        ('PERSONAL INFO', {'fields': ('gender','ciga', 'meet_path','phone1','phone2','phone3')}),
        ('PERMISSIONS', {'fields': ('is_active', 'is_staff', 'is_superuser','active','payment','user_type','connector')}),
    )
     
    # list page
    list_display = ['username','name', 'email','active','payment']
 
class CustomLikeAdmin(UserAdmin):
	model = Like
	list_display = ['username','Room_infos']
 
admin.site.register(User, CustomUserAdmin)
admin.site.register(Room_infos)
admin.site.register(Tags)
admin.site.register(Like)
admin.site.register(Connect)
admin.site.register(call_file)
admin.site.register(Complete_contract)