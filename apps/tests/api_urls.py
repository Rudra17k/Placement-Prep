from django.urls import path
from apps.tests.views import save_answer

urlpatterns = [
    path('tests/attempt/<int:attempt_id>/save-answer/', save_answer, name='save_answer'),
]
