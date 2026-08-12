from django.db import models
from django.contrib.auth.models import User


class Badge(models.Model):
    """Achievement badges earned by users."""

    CRITERIA_TYPES = [
        ('questions_solved', 'Total Questions Solved'),
        ('streak_days', 'Streak Days'),
        ('test_score', 'Test Score Percentage'),
        ('tests_completed', 'Tests Completed'),
        ('topic_mastery', 'Topic Mastery'),
        ('xp_earned', 'XP Earned'),
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=10, default='🏅')
    criteria_type = models.CharField(max_length=20, choices=CRITERIA_TYPES)
    criteria_value = models.IntegerField(
        help_text='Threshold value to earn this badge'
    )
    xp_reward = models.IntegerField(default=50, help_text='XP awarded when badge is earned')
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['criteria_type', 'criteria_value']

    def __str__(self):
        return f"{self.icon} {self.name}"


class UserBadge(models.Model):
    """Tracks which badges users have earned."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'badge']

    def __str__(self):
        return f"{self.user.email} — {self.badge.name}"


class DailyChallenge(models.Model):
    """Daily challenge questions."""

    date = models.DateField(unique=True)
    questions = models.ManyToManyField('questions.Question')
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    bonus_xp = models.IntegerField(default=100)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"Challenge — {self.date}"
