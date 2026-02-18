from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/health/', include('core.health.urls')),
    # Add other app urls here
    # path('api/oauth/', include('core.social.urls')),
    # path('api/posts/', include('core.posts.urls')),
    # etc.
]
