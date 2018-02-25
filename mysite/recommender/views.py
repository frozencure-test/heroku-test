from . import processor
from django.http import JsonResponse


def get_questions(request):
    context = {}
    if request.method == 'GET':
        question_id = request.GET.get('question_id')
        if question_id:
            questionResults = processor.getTopQuestions(question_id=int(question_id))
            if questionResults == False:
                return JsonResponse({'Error' : "Question has too few favourites or is doesn't exist"})
            context['question'] = questionResults
            return JsonResponse({'similarities' : questionResults})
        else:
            return JsonResponse({})
