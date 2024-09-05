from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='custom_admin_dashboard'),
    path('users/', views.user_list, name='custom_admin_user_list'),
    path('blog-posts/', views.blog_post_list, name='custom_admin_blog_post_list'),
    path('blog-posts/<int:pk>/edit/', views.blog_post_edit, name='custom_admin_blog_post_edit'),
    path('blog-posts/<int:pk>/delete/', views.blog_post_delete, name='custom_admin_blog_post_delete'),
    path('categories/', views.category_list, name='custom_admin_category_list'),
    path('tags/', views.tag_list, name='custom_admin_tag_list'),
]