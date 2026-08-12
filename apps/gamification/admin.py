from django.contrib import admin
from .models import Badge, UserBadge, DailyChallenge

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['icon', 'name', 'criteria_type', 'criteria_value', 'xp_reward', 'is_active']
    list_filter = ['criteria_type', 'is_active']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'earned_at']

@admin.register(DailyChallenge)
class DailyChallengeAdmin(admin.ModelAdmin):
    list_display = ['date', 'difficulty', 'bonus_xp']
    filter_horizontal = ['questions']
