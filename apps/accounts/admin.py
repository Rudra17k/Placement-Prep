from django.contrib import admin
from .models import UserProfile

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'college', 'branch', 'graduation_year', 'xp_points', 'streak_count', 'level']
    list_filter = ['graduation_year', 'preferred_language']
    search_fields = ['user__email', 'college', 'branch']
    readonly_fields = ['xp_points', 'streak_count', 'longest_streak', 'total_questions_attempted', 'total_questions_correct']

    def level(self, obj):
        return obj.level
