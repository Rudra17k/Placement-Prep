from django.contrib import admin
from .models import Topic, Question

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'icon', 'order', 'is_active']
    list_filter = ['category', 'is_active']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['short_text', 'topic', 'difficulty', 'times_attempted', 'success_rate', 'is_verified']
    list_filter = ['difficulty', 'topic__category', 'topic', 'is_verified', 'companies']
    search_fields = ['text']
    filter_horizontal = ['companies']

    def short_text(self, obj):
        return obj.text[:100]
    short_text.short_description = 'Question'
