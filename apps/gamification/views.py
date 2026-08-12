from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile


@login_required
def leaderboard(request):
    """Weekly/monthly/all-time leaderboard."""
    timeframe = request.GET.get('timeframe', 'all')
    top_users = UserProfile.objects.select_related('user').order_by('-xp_points')[:50]

    # Get current user's rank
    user_rank = UserProfile.objects.filter(
        xp_points__gt=request.user.profile.xp_points
    ).count() + 1

    context = {
        'top_users': top_users,
        'user_rank': user_rank,
        'timeframe': timeframe,
    }
    return render(request, 'pages/leaderboard.html', context)
