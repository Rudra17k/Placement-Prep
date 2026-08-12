from django.urls import path
from . import api_views

urlpatterns = [
    path('ai/hint/', api_views.get_ai_hint, name='api_ai_hint'),
    path('ai/ask/', api_views.ask_ai_doubt, name='api_ai_ask'),
]
