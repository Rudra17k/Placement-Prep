from django.urls import path
from . import api_views

urlpatterns = [
    path('insights/generate/', api_views.generate_insights, name='api_generate_insights'),
]
