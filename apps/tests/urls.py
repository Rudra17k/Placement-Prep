from django.urls import path
from . import views

urlpatterns = [
    path('tests/', views.test_list, name='test_list'),
    path('tests/<slug:slug>/start/', views.start_test, name='start_test'),
    path('tests/attempt/<int:attempt_id>/', views.take_test, name='take_test'),
    path('tests/attempt/<int:attempt_id>/submit/', views.submit_test, name='submit_test'),
    path('tests/attempt/<int:attempt_id>/results/', views.test_results, name='test_results'),
]
