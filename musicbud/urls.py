from django.contrib import admin
from django.urls import path, include
from app.views.auth_views import AuthLogin, register_view
from app.views.home_views import home
from chat.views import user_list, channel_list
from app.views.error_views import page_not_found_view, server_error_view # New Import

urlpatterns = [
    path('admin/', admin.site.urls),
    # Web UI routes (for Django templates)
    path('login/', AuthLogin.as_view(), name='login'),
    path('register/', register_view, name='register'),
    path('', home, name='home'),
    path('users/', user_list, name='user_list'),
    path('channels/', channel_list, name='channel_list'),
    
    # Legacy routes (without v1 prefix for backwards compatibility)
    path('', include('app.urls')),
    path('chat/', include('chat.urls', namespace='chat')), # Explicitly set for clarity
    
    # API v1 routes (recommended for Flutter app)
    path('v1/', include('app.urls')),
    path('v1/chat/', include('chat.urls', namespace='chat_v1')), # New unique namespace
]

handler404 = page_not_found_view
handler500 = server_error_view
