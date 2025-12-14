from django.shortcuts import render
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'

class RulesView(TemplateView):
    template_name = 'pages/rules.html'


def page_not_found(request, exception):
    """Вернуть 404."""
    return render(request, "pages/404.html", status=404)


def csrf_failure(request, reason=""):
    """Вернуть 403."""
    return render(request, "pages/403csrf.html", status=403)


def server_error(request, exception=None):
    """Вернуть 500."""
    return render(request, "pages/500.html", status=500)