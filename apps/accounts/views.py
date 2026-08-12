from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from apps.analytics.models import TopicMastery
from apps.tests.models import TestAttempt
from apps.questions.models import Topic


def landing_page(request):
    """Public landing page."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'pages/landing.html')


@login_required
def dashboard(request):
    """Student dashboard with stats, streaks, and recommendations."""
    profile = request.user.profile
    profile.update_streak()

    # Recent attempts
    recent_attempts = TestAttempt.objects.filter(
        user=request.user, is_completed=True
    ).select_related('test', 'test__company')[:5]

    # Topic mastery for radar chart
    mastery_data = TopicMastery.objects.filter(
        user=request.user
    ).select_related('topic').order_by('-mastery_score')

    # Weak topics (mastery < 0.4)
    weak_topics = mastery_data.filter(mastery_score__lt=0.4)[:5]

    # Strong topics (mastery > 0.7)
    strong_topics = mastery_data.filter(mastery_score__gt=0.7)[:5]

    # Category-wise stats
    categories = Topic.CATEGORY_CHOICES
    category_stats = []
    for cat_key, cat_name in categories:
        cat_mastery = mastery_data.filter(topic__category=cat_key)
        if cat_mastery.exists():
            avg = sum(m.mastery_score for m in cat_mastery) / len(cat_mastery)
        else:
            avg = 0
        category_stats.append({
            'key': cat_key,
            'name': cat_name,
            'mastery': round(avg * 100, 1),
        })

    context = {
        'profile': profile,
        'recent_attempts': recent_attempts,
        'mastery_data': mastery_data,
        'weak_topics': weak_topics,
        'strong_topics': strong_topics,
        'category_stats': category_stats,
    }
    return render(request, 'pages/dashboard.html', context)


@login_required
def profile_view(request):
    """User profile page."""
    profile = request.user.profile
    if request.method == 'POST':
        profile.college = request.POST.get('college', '')
        profile.branch = request.POST.get('branch', '')
        year = request.POST.get('graduation_year', '')
        if year:
            profile.graduation_year = int(year)
        profile.preferred_language = request.POST.get('preferred_language', 'en')
        profile.save()
        return redirect('profile')

    return render(request, 'pages/profile.html', {'profile': profile})
