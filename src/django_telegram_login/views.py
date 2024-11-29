__all__ = (
    'page_not_found_view',
)

import os
from django.conf import settings
from django.http import FileResponse
from django.shortcuts import render


def page_not_found_view(request, exception):
    """ Функция обработки ошибки 404 """
    return render(request, 'layout/404.html', status=404)
