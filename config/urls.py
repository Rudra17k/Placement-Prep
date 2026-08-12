"""PlacePrep AI URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('apps.accounts.urls')),
    path('', include('apps.questions.urls')),
    path('', include('apps.companies.urls')),
    path('', include('apps.tests.urls')),
    path('', include('apps.analytics.urls')),
    path('', include('apps.gamification.urls')),
    path('api/', include('apps.questions.api_urls')),
    path('api/', include('apps.tests.api_urls')),
    path('api/', include('apps.analytics.api_urls')),
    path('api/', include('apps.ai_engine.api_urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
