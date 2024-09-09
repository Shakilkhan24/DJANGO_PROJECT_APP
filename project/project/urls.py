from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views  # Import Django's built-in auth views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),        # Default Django admin interface
    # path('custom-admin/', include('custom_admin.urls')),  # Custom admin application
    path('', include('app.urls')),          # Your app's URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Ensure login view is accessible
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Ensure logout view is accessible
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)