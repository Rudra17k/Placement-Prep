from django.db import models


class Topic(models.Model):
    """Question categories and topics."""

    CATEGORY_CHOICES = [
        ('aptitude', 'Quantitative Aptitude'),
        ('reasoning', 'Logical Reasoning'),
        ('verbal', 'Verbal Ability'),
        ('di', 'Data Interpretation'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    icon = models.CharField(max_length=10, default='📝')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['category', 'order', 'name']

    def __str__(self):
        return f"{self.get_category_display()} → {self.name}"


class Question(models.Model):
    """Individual practice questions."""

    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('medium', 'Medium'),
        ('hard', 'Hard'),
    ]

    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='questions')
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='medium')

    # Question content (bilingual)
    text = models.TextField(help_text='Question text in English')
    text_hi = models.TextField(blank=True, help_text='Question text in Hindi')
    image = models.ImageField(upload_to='questions/', blank=True, null=True)

    # Options stored as JSON: [{"key":"A","text":"...","text_hi":"..."}]
    options = models.JSONField(
        help_text='List of options: [{"key":"A","text":"Option text","text_hi":"..."}]'
    )
    correct_option = models.CharField(max_length=1)

    # Explanations
    explanation = models.TextField(blank=True, help_text='Detailed explanation in English')
    explanation_hi = models.TextField(blank=True, help_text='Explanation in Hindi')
    shortcut_method = models.TextField(blank=True, help_text='Quick solving trick')
    ai_explanation = models.TextField(blank=True, help_text='Cached AI-generated explanation')

    # Metadata
    companies = models.ManyToManyField(
        'companies.Company', blank=True, related_name='questions'
    )
    source = models.CharField(max_length=200, blank=True, help_text='Where this question is from')
    year = models.IntegerField(null=True, blank=True)

    # Stats (denormalized for performance)
    times_attempted = models.IntegerField(default=0)
    times_correct = models.IntegerField(default=0)
    elo_rating = models.FloatField(default=1200.0, help_text='Adaptive difficulty rating')

    is_verified = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['topic', 'difficulty']),
            models.Index(fields=['elo_rating']),
            models.Index(fields=['difficulty', 'is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.difficulty}] {self.text[:80]}..."

    @property
    def success_rate(self):
        if self.times_attempted == 0:
            return 0
        return round((self.times_correct / self.times_attempted) * 100, 1)
