from django.contrib import admin
from .models import TopicMastery

@admin.register(TopicMastery)
class TopicMasteryAdmin(admin.ModelAdmin):
    list_display = ['user', 'topic', 'mastery_percent', 'questions_attempted', 'accuracy']
    list_filter = ['topic__category', 'topic']
