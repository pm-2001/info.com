from re import template
from django.contrib import admin
from django.urls import path
from blog import views
from blog.views import PostDetail,UpdatePostView,DeletePostView,LikeView,PasswordsChangeView,AddCategoryView,CategoryView
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.home, name='home'),
    path('article/<int:pk>',PostDetail.as_view(),name='postdetail'),
    path('about',views.about, name='about'),
    path('contact',views.contact, name='contact'),
    path('profile/<int:pk>',views.profile, name='profile'),
    path('posts/',views.posts, name='posts'),
    path('add_category/',AddCategoryView.as_view(), name='add_category'),
    path('category/<str:cats>/',CategoryView, name='category'),
    path('register',views.register, name='register'),
    path('edit_profile/',views.editprofile, name='edit_profile'),
    # path('password/', auth_views.PasswordChangeView.as_view(template_name='change_password.html')),
    path('password/',PasswordsChangeView.as_view(template_name='change_password.html')),
    path('password_success',views.password_success, name='password_success'),
    path('signin',views.signin, name='signin'),
    path('logout',views.logoutUser, name='logout'),
    path('article/edit/<int:pk>',views.UpdatePostView.as_view(),name='update_post'),
    path('article/delete/<int:pk>',views.DeletePostView.as_view(),name='delete_post'),
    path('myblogs',views.myblogs, name='myblogs'),
    path('like/<int:pk>',LikeView , name='like_post'),
    # path('article/<int:pk>/comment/', AddCommentView.as_view(), name='addcomment'),
    # path('delete/<post_id>',views.delete_post,name='delete'),
]