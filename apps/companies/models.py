from django.db import models


class Company(models.Model):
    """Companies that conduct placement drives."""

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    logo_emoji = models.CharField(max_length=10, default='🏢')
    description = models.TextField(blank=True)
    website = models.URLField(blank=True)
    exam_pattern = models.JSONField(
        default=dict, blank=True,
        help_text='JSON describing the exam structure, sections, and timing'
    )
    avg_package_lpa = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True,
        help_text='Average package in LPA'
    )
    eligibility_criteria = models.TextField(blank=True)
    difficulty_level = models.CharField(
        max_length=10,
        choices=[('easy', 'Easy'), ('medium', 'Medium'), ('hard', 'Hard')],
        default='medium'
    )
    is_active = models.BooleanField(default=True)
    total_questions = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['name']

    def __str__(self):
        return self.name
