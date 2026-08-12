import json
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import JsonResponse
from .models import MockTest, TestAttempt, AttemptAnswer, TestQuestion


@login_required
def test_list(request):
    """Available mock tests."""
    tests = MockTest.objects.filter(is_published=True).select_related('company')
    return render(request, 'pages/test_list.html', {'tests': tests})


@login_required
def start_test(request, slug):
    """Start a new test attempt."""
    test = get_object_or_404(MockTest, slug=slug, is_published=True)

    # Create attempt
    attempt = TestAttempt.objects.create(
        user=request.user,
        test=test,
        total_questions=test.test_questions.count()
    )

    # Create answer slots
    for tq in test.test_questions.select_related('question').all():
        AttemptAnswer.objects.create(
            attempt=attempt,
            question=tq.question
        )

    return redirect('take_test', attempt_id=attempt.id)


@login_required
def take_test(request, attempt_id):
    """Test-taking interface with timer."""
    attempt = get_object_or_404(
        TestAttempt, id=attempt_id, user=request.user, is_completed=False
    )
    test = attempt.test
    questions = test.test_questions.select_related('question').order_by('order')
    answers = {a.question_id: a for a in attempt.answers.all()}

    # Calculate remaining time
    elapsed = (timezone.now() - attempt.started_at).total_seconds()
    remaining = max(0, test.duration_minutes * 60 - elapsed)

    context = {
        'attempt': attempt,
        'test': test,
        'questions': questions,
        'answers': answers,
        'remaining_seconds': int(remaining),
    }
    return render(request, 'pages/take_test.html', context)


@login_required
def save_answer(request, attempt_id):
    """AJAX endpoint to save individual answers during test."""
    if request.method != 'POST':
        return JsonResponse({'error': 'POST required'}, status=405)

    attempt = get_object_or_404(
        TestAttempt, id=attempt_id, user=request.user, is_completed=False
    )

    data = json.loads(request.body)
    question_id = data.get('question_id')
    selected = data.get('selected_option', '')

    try:
        answer = AttemptAnswer.objects.get(attempt=attempt, question_id=question_id)
        answer.selected_option = selected
        answer.is_answered = bool(selected)
        answer.is_correct = selected == answer.question.correct_option
        answer.save()
        return JsonResponse({'status': 'saved'})
    except AttemptAnswer.DoesNotExist:
        return JsonResponse({'error': 'Invalid question'}, status=400)


@login_required
def submit_test(request, attempt_id):
    """Submit a test and calculate results."""
    attempt = get_object_or_404(
        TestAttempt, id=attempt_id, user=request.user, is_completed=False
    )

    # Calculate results
    answers = attempt.answers.select_related('question').all()
    correct = sum(1 for a in answers if a.is_correct)
    wrong = sum(1 for a in answers if a.is_answered and not a.is_correct)
    unanswered = sum(1 for a in answers if not a.is_answered)

    elapsed = (timezone.now() - attempt.started_at).total_seconds()

    attempt.completed_at = timezone.now()
    attempt.is_completed = True
    attempt.correct_answers = correct
    attempt.wrong_answers = wrong
    attempt.unanswered = unanswered
    attempt.time_taken_seconds = int(elapsed)
    attempt.total_questions = answers.count()

    # Score calculation
    if attempt.test.negative_marking:
        attempt.score = max(0, correct - int(wrong * attempt.test.negative_marks))
    else:
        attempt.score = correct

    attempt.percentage = round((correct / attempt.total_questions) * 100, 1) if attempt.total_questions else 0

    # XP calculation
    xp = int(attempt.percentage / 10) * 5  # 5 XP per 10%
    attempt.xp_earned = xp
    attempt.save()

    # Update user profile
    profile = request.user.profile
    profile.total_tests_taken += 1
    profile.xp_points += xp
    profile.update_streak()
    profile.save()

    # Update test stats
    test = attempt.test
    test.times_taken += 1
    all_attempts = test.attempts.filter(is_completed=True)
    test.avg_score = sum(a.percentage for a in all_attempts) / all_attempts.count()
    test.save()

    # Update question stats and topic mastery
    for answer in answers:
        q = answer.question
        q.times_attempted += 1
        if answer.is_correct:
            q.times_correct += 1
        q.save(update_fields=['times_attempted', 'times_correct'])

    return redirect('test_results', attempt_id=attempt.id)


@login_required
def test_results(request, attempt_id):
    """Test results and review page."""
    attempt = get_object_or_404(
        TestAttempt, id=attempt_id, user=request.user, is_completed=True
    )
    answers = attempt.answers.select_related('question', 'question__topic').order_by('question__in_tests__order')

    context = {
        'attempt': attempt,
        'answers': answers,
    }
    return render(request, 'pages/test_results.html', context)
