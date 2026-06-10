from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('logbook/', include('logbook.urls')),
    path('evaluation/', include('evaluation.urls')),
    path('api/accounts/', include('accounts.api.urls')),
    path('api/logbook/', include('logbook.api.urls')),
    path('api/evaluation/', include('evaluation.api.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
