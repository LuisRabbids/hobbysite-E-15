"""
URL configuration for hobbysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import include, path
from .views import homepage # Import the new homepage view
from django.conf import settings # For media files
from django.conf.urls.static import static # For media files

from django.contrib import admin
from django.urls import include, path
from .views import homepage, register # Add register

urlpatterns = [
    path('', homepage, name='homepage'),  # Homepage at root

    path('accounts/', include('django.contrib.auth.urls')),  # Django auth URLs (login, logout, password reset etc.)
    path('accounts/register/', register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),
    
    # Your app URLs
    path('merchstore/', include('merchstore.urls')),
    path('wiki/', include(('wiki.urls', 'wiki'), namespace='wiki')),  # Added namespace
    path('blog/', include('blog.urls')),
    path('forum/', include('forum.urls')),
    path('commissions/', include('commissions.urls')),
    path('admin/', admin.site.urls),
]
# For serving media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)