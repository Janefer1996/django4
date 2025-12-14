from django.urls import path

from .views import AboutView, RulesView


app_name = 'pages'

urlpatterns = [
    path('pages/about/', AboutView.as_view(), name='about'),
    path('pages/rules/', RulesView.as_view(), name='rules'),
]
