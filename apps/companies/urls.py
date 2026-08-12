from django.urls import path
from . import views

urlpatterns = [
    path('companies/', views.company_list, name='company_list'),
    path('companies/<slug:slug>/', views.company_detail, name='company_detail'),
]
