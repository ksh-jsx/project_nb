from django.urls import path,re_path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('mail_authenticate', views.mail_authenticate, name='mail_authenticate'),
    path('activate/<str:uid64>/<str:token>', views.activate, name='activate'),
    path('search_univ/', views.search_univ, name='search_univ'),
    path('search_univ/detail/', views.item_detail, name='item_detail'),
    path('payment/', views.payment, name='payment'),
    path('blog', views.post_list, name='post_list'),
    path('blog/post/<int:pk>/', views.post_detail, name='post_detail'),
    path('blog/post/new/', views.post_new, name='post_new'),
    path('blog/post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    
    re_path(r'^like/$', views.post_like, name='post_like'),
    re_path(r'^sort/$', views.sort, name='sort'),
    re_path(r'^blog/post/(?P<pk>\d+)/remove/$', views.post_remove, name='post_remove'),
    re_path(r'^blog/post/(?P<pk>\d+)/comment/$', views.add_comment_to_post, name='add_comment_to_post'),
    re_path(r'^blog/email_to_admin/$', views.email_to_admin, name='email_to_admin'),

    path('accounts/find_username/',views.find_username,name='find_user'),
    path('accounts/signup/', views.SignUp.as_view(), name='signup'),
    path('accounts/signup_success/', TemplateView.as_view(template_name='registration/signup_success.html'), name='signup_success'),
    path('test', views.test, name='test'),
    
]

