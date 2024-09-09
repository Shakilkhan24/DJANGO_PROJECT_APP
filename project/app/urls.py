from django.urls import path
from . import views
from app.views import custom_logout_view
from app.views import CustomLoginView


urlpatterns = [
    path('', views.blog_list, name='home'),
    path('signup/', views.signup, name='signup'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/logout/', custom_logout_view, name='logout'),
    path('profile/', views.user_profile, name='user_profile'),  # This should match
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('blog/',views.blog_list,name='blog_list'),
    path('blog/create/', views.blog_create, name='blog_create'),
    path('blog/<pk>/', views.blog_detail, name='blog_detail'),
    path('blog/<pk>/edit/', views.blog_edit, name='blog_edit'),
    path('blog/<pk>/delete/', views.blog_delete, name='blog_delete'),
    path('tag/', views.tag_list, name='tag_list'),
    path('tag/<pk>/', views.tag_detail, name='tag_detail'),
    path('search/', views.search, name='search'),
]

