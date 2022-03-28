"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import (path, re_path, include)
from allauth.account import views
from django.contrib.auth.views import LoginView,LogoutView
#from blog.views import SocialLoginCallbackView

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    path('user/', include('blog.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/',include('allauth.urls')),
    
    re_path(r"^accounts/password/reset/$", views.password_reset,name="account_reset_password"),
    re_path(r"^password/reset/done/$", views.password_reset_done,name="account_reset_password_done"),
    re_path(r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",views.password_reset_from_key,name="account_reset_password_from_key"),
    re_path(r"^password/reset/key/done/$", views.password_reset_from_key_done,name="account_reset_password_from_key_done"),
    
    re_path(r'^accounts/login/$',  views.login, name='login'),
    re_path(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    #path('accounts/login/<provider>/callback/', SocialLoginCallbackView.as_view()),
    re_path(r'', include('blog.urls')),
    
    
]
