from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class MockTest(models.Model):
    """Pre-configured tests and mock OA simulations."""

    TEST_TYPE_CHOICES = [
        ('practice', 'Practice Test'),
        ('mock', 'Mock OA'),
        ('daily', 'Daily Challenge'),
        ('custom', 'Custom Test'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    company = models.ForeignKey(
        'companies.Company', null=True, blank=True,
        on_delete=models.SET_NULL, related_name='mock_tests'
    )
    test_type = models.CharField(max_length=10, choices=TEST_TYPE_CHOICES, default='practice')
    duration_minutes = models.IntegerField(default=30)
    total_questions = models.IntegerField(default=20)
    passing_score = models.IntegerField(default=60, help_text='Percentage required to pass')
    negative_marking = models.BooleanField(default=False)
    negative_marks = models.FloatField(default=0.25, help_text='Marks deducted per wrong answer')
    difficulty = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard'), ('mixed', 'Mixed')],
        default='mixed'
    )
    instructions = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    times_taken = models.IntegerField(default=0)
    avg_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TestQuestion(models.Model):
    """Links questions to tests with ordering."""
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='test_questions')
    question = models.ForeignKey(
        'questions.Question', on_delete=models.CASCADE, related_name='in_tests'
    )
    order = models.IntegerField(default=0)
    section = models.CharField(max_length=50, blank=True)

    class Meta:
        ordering = ['order']
        unique_together = ['test', 'question']

    def __str__(self):
        return f"{self.test.title} — Q{self.order}"


class TestAttempt(models.Model):
    """Records a user's attempt at a test."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='test_attempts')
    test = models.ForeignKey(MockTest, on_delete=models.CASCADE, related_name='attempts')
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)

    # Results
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=0)
    correct_answers = models.IntegerField(default=0)
    wrong_answers = models.IntegerField(default=0)
    unanswered = models.IntegerField(default=0)
    time_taken_seconds = models.IntegerField(null=True, blank=True)
    percentage = models.FloatField(default=0)

    # XP earned for this attempt
    xp_earned = models.IntegerField(default=0)

    class Meta:
        ordering = ['-started_at']
        indexes = [
            models.Index(fields=['user', '-completed_at']),
            models.Index(fields=['user', 'test']),
        ]

    def __str__(self):
        status = "✓" if self.is_completed else "…"
        return f"{status} {self.user.email} — {self.test.title}"

    @property
    def duration_display(self):
        if not self.time_taken_seconds:
            return "N/A"
        mins = self.time_taken_seconds // 60
        secs = self.time_taken_seconds % 60
        return f"{mins}m {secs}s"


class AttemptAnswer(models.Model):
    """Individual question answers within a test attempt."""

    attempt = models.ForeignKey(
        TestAttempt, on_delete=models.CASCADE, related_name='answers'
    )
    question = models.ForeignKey(
        'questions.Question', on_delete=models.CASCADE
    )
    selected_option = models.CharField(max_length=1, blank=True)
    is_correct = models.BooleanField(default=False)
    is_answered = models.BooleanField(default=False)
    time_taken_seconds = models.IntegerField(default=0)
    is_flagged = models.BooleanField(default=False, help_text='Flagged for review')

    class Meta:
        unique_together = ['attempt', 'question']

    def __str__(self):
        return f"{'✓' if self.is_correct else '✗'} Q{self.question.id}"
