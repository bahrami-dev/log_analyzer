from django.urls import path

from .views import parser

urlpatterns = [
    path('parse', parser, name='parser'),
]
