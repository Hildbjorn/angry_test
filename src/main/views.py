from django.shortcuts import render
from django.views.generic import TemplateView

__all__ = (
    'IndexPageView',
)

class IndexPageView(TemplateView):
    template_name = 'main/index.html'