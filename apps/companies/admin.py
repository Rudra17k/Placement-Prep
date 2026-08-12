from django.contrib import admin
from .models import Company

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'difficulty_level', 'avg_package_lpa', 'total_questions', 'is_active']
    list_filter = ['difficulty_level', 'is_active']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}
