from django.contrib import admin
from .models import MockTest, TestQuestion, TestAttempt, AttemptAnswer

class TestQuestionInline(admin.TabularInline):
    model = TestQuestion
    extra = 1

@admin.register(MockTest)
class MockTestAdmin(admin.ModelAdmin):
    list_display = ['title', 'test_type', 'company', 'duration_minutes', 'total_questions', 'times_taken', 'is_published']
    list_filter = ['test_type', 'company', 'is_published', 'difficulty']
    prepopulated_fields = {'slug': ('title',)}
    inlines = [TestQuestionInline]

@admin.register(TestAttempt)
class TestAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'test', 'score', 'percentage', 'is_completed', 'started_at']
    list_filter = ['is_completed', 'test']
    readonly_fields = ['score', 'correct_answers', 'wrong_answers', 'percentage', 'xp_earned']
