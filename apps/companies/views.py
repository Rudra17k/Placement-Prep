from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Company


@login_required
def company_list(request):
    """Grid of companies with placement info."""
    companies = Company.objects.filter(is_active=True)
    return render(request, 'pages/companies.html', {'companies': companies})


@login_required
def company_detail(request, slug):
    """Company detail with exam pattern and mock tests."""
    company = get_object_or_404(Company, slug=slug, is_active=True)
    mock_tests = company.mock_tests.filter(is_published=True)
    questions = company.questions.filter(is_active=True)[:10]

    context = {
        'company': company,
        'mock_tests': mock_tests,
        'recent_questions': questions,
    }
    return render(request, 'pages/company_detail.html', context)
