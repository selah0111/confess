from django.contrib import admin
from django.urls import path
from account import views
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from account.views import (PostCreateView,PostDeleteView,PicDeleteView,Search_User,about,ProfileListView,PostUpdateView,userEdit,userSetting
)


urlpatterns = [
    path('', views.home, name='confessions-home'),
    path('signup/', views.signup, name='signup'),
    path('login', views.user_login, name='login'),
    path('logout', views.user_logout, name='logout'),
    url(r'c/ph/$',views.pic_list,name="pic_list"),
    url(r'c/d/(?P<id>\d+)[\w-]+/$', views.pic_detail ,name='detail'),
    url(r'c/prd/(?P<id>\d+)[\w-]+/$', views.pro_detail ,name='pro-detail'),
    url(r'^c/pd/(?P<id>\d+)[\w-]+/$', views.post_detail, name="confessions-detail"),
    path('c/n', views.PostCreateView, name="conpost"),
    path('c/<int:pk>/update/', PostUpdateView.as_view(), name="confessions-update"),
    path('c/<int:pk>/delete/', PostDeleteView.as_view(), name="confessions-delete"),
    path('c/d/delete/<int:pk>/', PicDeleteView.as_view(), name="pic-delete"),
    path('pp/',views.picpost, name="picpost"), 
    path('account/about/',views.about, name="about"), 
    url(r'^like/$',views.like_post, name="like"),
    path("<str:username>/", views.userProfile, name='user_profile'),
    path("<int:pk>/edit_profile", userEdit.as_view(), name='edit_profile'),
    path("<int:pk>/setting", userSetting.as_view(), name='setting'),
    path("user/follow/<str:username>", views.follow, name="follow"),
    path("account/search/", Search_User.as_view(), name="search_user"),
    path('profiles/account/' ,ProfileListView.as_view(),name='plv'),
    path('account/pc/d/', auth_views.PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'),name='password_change_done'), 
    path('account/pc/', auth_views.PasswordChangeView.as_view(template_name='users/password_change.html'), name='password_change'),
    path('account/password_reset/',auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),name="password_reset"),
    path('account/password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),name="password_reset_done"),
    path('account/password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name="password_reset_confirm"),
    path('account/password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name="password_reset_complete"),

    ]