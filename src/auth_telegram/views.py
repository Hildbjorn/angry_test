from django.http import JsonResponse
from django.views.generic import TemplateView


__all__ = (
    'IndexPageView',
    'check_auth',
)

class IndexPageView(TemplateView):
    template_name = 'auth_telegram/index.html'

def check_auth(request):
    """ Возвращаем JSON-ответ с информацией об авторизации пользователя """
    return JsonResponse({'is_authenticated': request.user.is_authenticated})