from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile for placement preparation."""

    LANGUAGE_CHOICES = [
        ('en', 'English'),
        ('hi', 'Hindi'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    college = models.CharField(max_length=200, blank=True)
    branch = models.CharField(max_length=100, blank=True)
    graduation_year = models.IntegerField(null=True, blank=True)
    target_companies = models.ManyToManyField(
        'companies.Company', blank=True, related_name='targeting_students'
    )
    preferred_language = models.CharField(
        max_length=5, choices=LANGUAGE_CHOICES, default='en'
    )

    # Gamification
    xp_points = models.IntegerField(default=0)
    streak_count = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)

    # Stats cache (updated periodically)
    total_questions_attempted = models.IntegerField(default=0)
    total_questions_correct = models.IntegerField(default=0)
    total_tests_taken = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.email} — {self.college or 'No college'}"

    @property
    def accuracy_percent(self):
        if self.total_questions_attempted == 0:
            return 0
        return round(
            (self.total_questions_correct / self.total_questions_attempted) * 100, 1
        )

    @property
    def level(self):
        """Calculate level from XP (every 500 XP = 1 level)."""
        return (self.xp_points // 500) + 1

    def update_streak(self):
        """Update daily streak."""
        today = timezone.now().date()
        if self.last_active_date == today:
            return  # Already active today

        if self.last_active_date == today - timezone.timedelta(days=1):
            self.streak_count += 1
        else:
            self.streak_count = 1

        if self.streak_count > self.longest_streak:
            self.longest_streak = self.streak_count

        self.last_active_date = today
        self.save(update_fields=[
            'streak_count', 'longest_streak', 'last_active_date'
        ])


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Auto-create profile when user is created."""
    if created:
        UserProfile.objects.create(user=instance)
