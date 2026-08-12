from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from apps.analytics.models import TopicMastery
from apps.ai_engine.services import AIEngineService

@login_required
def generate_insights(request):
    """
    API endpoint that fetches user mastery data and uses the AI Engine to generate study insights.
    """
    profile = request.user.profile
    
    # Fetch mastery data
    mastery_data = TopicMastery.objects.filter(
        user=request.user
    ).select_related('topic').order_by('-mastery_score')

    weak_topics = list(mastery_data.filter(mastery_score__lt=0.4)[:3])
    strong_topics = list(mastery_data.filter(mastery_score__gt=0.7)[:3])

    insight_text = AIEngineService.generate_personalized_insights(
        weak_topics=weak_topics,
        strong_topics=strong_topics,
        user_level=profile.level,
        streak=profile.streak_count
    )

    return JsonResponse({
        'status': 'success',
        'insight': insight_text
    })
