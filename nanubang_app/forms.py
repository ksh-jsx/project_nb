from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm)
from .models import User,Room_infos,Tags,call_file


class UserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username','ciga', 'email', 'name', 'phone1', 'phone2', 'phone3', 'gender', 'mail_agree', 'sms_agree', 'meet_path')


class UserChangeForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','ciga', 'email', 'name', 'phone1', 'phone2','gender', 'phone3', 'active')

class Room_infosForm(forms.ModelForm):

    class Meta:
        model = Room_infos
        fields = ('address', 'address_detail','univ','tag','room_type','deposit','monthly_cost','deposit_necessity','desired_deposit',
                  'desired_monthly','management_cost_include','management_cost','start_date','end_date','floor','sublessee_type1','sublessee_type2',
                  'room_options','sublessor_type1','sublessor_type2','room_desc','room_size','is_duplex','window','latitude','longitude','photo1','photo2','photo3','photo4','pano_photo')

class call_fileForm(forms.ModelForm):

    class Meta:
        model =  call_file
        fields = ('file1',)

class TagsForm(forms.ModelForm):

    class Meta:
        model = Tags
        fields = ('tag','univ')
