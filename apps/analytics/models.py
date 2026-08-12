from django.db import models
from django.contrib.auth.models import User


class TopicMastery(models.Model):
    """Tracks per-user, per-topic proficiency — updated after each attempt."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topic_mastery')
    topic = models.ForeignKey('questions.Topic', on_delete=models.CASCADE)
    mastery_score = models.FloatField(
        default=0.0, help_text='0.0 to 1.0 proficiency score'
    )
    questions_attempted = models.IntegerField(default=0)
    questions_correct = models.IntegerField(default=0)
    avg_time_seconds = models.FloatField(default=0)
    last_practiced = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ['user', 'topic']
        verbose_name_plural = 'Topic Mastery'
        indexes = [
            models.Index(fields=['user', 'mastery_score']),
        ]

    def __str__(self):
        return f"{self.user.email} — {self.topic.name}: {self.mastery_percent}%"

    @property
    def mastery_percent(self):
        return round(self.mastery_score * 100, 1)

    @property
    def accuracy(self):
        if self.questions_attempted == 0:
            return 0
        return round((self.questions_correct / self.questions_attempted) * 100, 1)
