from django.urls import path
from . import views

urlpatterns = [
    path('practice/', views.practice_home, name='practice'),
    path('practice/<slug:slug>/', views.topic_questions, name='topic_questions'),
    path('question/<int:pk>/', views.question_detail, name='question_detail'),
]
