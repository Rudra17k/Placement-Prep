from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Topic, Question
from apps.analytics.models import TopicMastery


@login_required
def practice_home(request):
    """Topic selection grid grouped by category."""
    categories = []
    for cat_key, cat_name in Topic.CATEGORY_CHOICES:
        topics = Topic.objects.filter(category=cat_key, is_active=True).annotate(
            q_count=models.Count('questions', filter=models.Q(questions__is_active=True))
        )
        categories.append({
            'key': cat_key,
            'name': cat_name,
            'topics': topics,
        })
    return render(request, 'pages/practice.html', {'categories': categories})


@login_required
def topic_questions(request, slug):
    """List questions for a topic with filters."""
    topic = get_object_or_404(Topic, slug=slug)
    difficulty = request.GET.get('difficulty', '')
    questions = Question.objects.filter(topic=topic, is_active=True)

    if difficulty:
        questions = questions.filter(difficulty=difficulty)

    # Get user mastery for this topic
    mastery, _ = TopicMastery.objects.get_or_create(
        user=request.user, topic=topic
    )

    context = {
        'topic': topic,
        'questions': questions,
        'mastery': mastery,
        'current_difficulty': difficulty,
    }
    return render(request, 'pages/topic_questions.html', context)


@login_required
def question_detail(request, pk):
    """Single question practice view."""
    question = get_object_or_404(Question, pk=pk, is_active=True)
    user_answered = False
    selected = ''
    is_correct = False

    if request.method == 'POST':
        selected = request.POST.get('answer', '')
        is_correct = selected == question.correct_option
        user_answered = True

        # Update question stats
        question.times_attempted += 1
        if is_correct:
            question.times_correct += 1
        question.save(update_fields=['times_attempted', 'times_correct'])

        # Update topic mastery
        mastery, _ = TopicMastery.objects.get_or_create(
            user=request.user, topic=question.topic
        )
        mastery.questions_attempted += 1
        if is_correct:
            mastery.questions_correct += 1
        mastery.mastery_score = mastery.questions_correct / mastery.questions_attempted
        mastery.save()

        # Update profile stats
        profile = request.user.profile
        profile.total_questions_attempted += 1
        if is_correct:
            profile.total_questions_correct += 1
            xp = {'easy': 10, 'medium': 25, 'hard': 50}.get(question.difficulty, 10)
            profile.xp_points += xp
        profile.update_streak()
        profile.save()

    # Get next question
    next_q = Question.objects.filter(
        topic=question.topic, is_active=True, pk__gt=question.pk
    ).first()

    context = {
        'question': question,
        'user_answered': user_answered,
        'selected': selected,
        'is_correct': is_correct,
        'next_question': next_q,
    }
    return render(request, 'pages/question_detail.html', context)


# Need to import models for annotation
from django.db import models
