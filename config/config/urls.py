from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static
from .views import home
from services.views import service_track_public

urlpatterns = [
    # Public Website & Tracking
    path('', home, name='home'),
    path('track/', service_track_public, name='track'),

    # Django Admin
    path('admin/', admin.site.urls),

    # Core System Modules
    path('service/', include('accounts.urls')),
    path('service/customers/', include('customers.urls')),
    path('service/', include('services.urls')),
    path('service/ledger/', include('ledger.urls')),
    path('service/notifications/', include('notification.urls')),

    # Backwards compatibility
    path('accounts/', include('accounts.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)