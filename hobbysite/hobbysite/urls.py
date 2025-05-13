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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from .views import homepage # Import the new homepage view
from django.conf import settings # For media files
from django.conf.urls.static import static # For media files
from .views import homepage, register # Add register

# hobbysite/urls.py

"""
URL configuration for hobbysite project.
"""
from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

from .views import homepage, register  # Assuming these exist in hobbysite/views.py

urlpatterns = [
    path('', homepage, name='homepage'),  # If you want the homepage view at root
    path('register/', register, name='register'),  # If register is a view
    path('merchstore/', include('merchstore.urls')),
    path('wiki/', include('wiki.urls')),
    path('blog/', include('blog.urls')),
    path('forum/', include('forum.urls')),
    path('commissions/', include('commissions.urls')),
    path('profile/', include('user_management.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
