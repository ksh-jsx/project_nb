from django.contrib import admin
from django.urls import path, include
from nanubang_app import views
from django.views.generic import TemplateView
from allauth.account import views as auth_views
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView

from django.conf.urls.static import static  # 추가
from django.conf import settings  # 추가

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('nanubang', views.nanubang, name='nanubang'),
    
    #방 동록,보기
    path('register/index', views.register_index, name='register_index'),
    path('register/main', views.register, name='register'),
    path('register/complete', views.register_complete, name='register_complete'),
    path('search_univ/', views.search_univ, name='search_univ'),
    path('like/', views.post_like, name='post_like'), # 좋아요 ajax
    path('room_detail/', views.room_detail, name='room_detail'),
    path('room_detail_temp/', views.room_detail_temp, name='room_detail_temp'),

    #계약
    path('contract_desc', views.contract_desc, name='contract_desc'),
    path('contract/1', views.contract1, name='contract1'),
    path('contract_type', views.contract_type, name='contract_type'),
    path('contract_confirm', views.contract_confirm, name='contract_confirm'),
    path('contract/2', views.contract2, name='contract2'),
    path('contract/3', views.contract3, name='contract3'),
	path('contract/4', views.contract4, name='contract4'),
    path('save_file', views.save_file, name='save_file'),
    path('contract_send1', views.send_contract1, name='send_contract1'),
    path('payment/', views.payment, name='payment'),
    path('payment/check', views.payment_check, name='payment_check'),

    #이메일 인증
    path('mail_authenticate', views.mail_authenticate, name='mail_authenticate'),
    path('activate/<str:uid64>/<str:token>', views.activate, name='activate'),
    path('check_authentication', views.check_authenticate, name='check'),
    
    #내정보, 고객센터
    path('mypage/', views.mypage, name='mypage'),
    path('cust_service/', views.cust_service, name = 'cust_serv'),
    path('cust_service<int:page>/', views.cust_service),

    #비밀번호 찾기
    path('accounts/password/reset/', auth_views.password_reset, name = 'account_reset_password'),
    path('accounts/password/reset/done', auth_views.password_reset_done, name = 'account_reset_password_done'),

    #계정
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path('accounts/signup', views.SignUp.as_view(), name='signup'),
    path('accounts/signup_success/', TemplateView.as_view(template_name='registration/signup_success.html'), name='signup_success'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('allauth.urls')),

    #삭제
    path('delete_user/', views.delete_user, name='delete_user'),
    path('delete_item/', views.delete_item, name='delete_item'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
