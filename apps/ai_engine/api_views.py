import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from apps.questions.models import Question
from apps.ai_engine.services import AIEngineService

@login_required
@csrf_exempt
def get_ai_hint(request):
    """
    API endpoint to return a Socratic hint for a question.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        question = Question.objects.get(pk=question_id)

        options_str = ", ".join([f"{opt['key']}: {opt['text']}" for opt in question.options])
        hint_text = AIEngineService.generate_socratic_hint(
            question_text=question.text,
            options_str=options_str
        )

        return JsonResponse({
            'status': 'success',
            'hint': hint_text
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required
@csrf_exempt
def ask_ai_doubt(request):
    """
    API endpoint for interactive Q&A regarding a question.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=400)

    try:
        data = json.loads(request.body)
        question_id = data.get('question_id')
        user_query = data.get('query', '').strip()

        if not user_query:
            return JsonResponse({'status': 'error', 'message': 'Query cannot be empty'}, status=400)

        question = Question.objects.get(pk=question_id)
        options_str = ", ".join([f"{opt['key']}: {opt['text']}" for opt in question.options])

        answer_text = AIEngineService.answer_question_doubt(
            question_text=question.text,
            options_str=options_str,
            explanation=question.explanation or "",
            user_query=user_query
        )

        return JsonResponse({
            'status': 'success',
            'answer': answer_text
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)
