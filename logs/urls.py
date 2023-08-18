from django.urls import path

from .views import parser, FileUploadView

urlpatterns = [
    path('parse', parser, name='parser'),
    path('upload/', FileUploadView.as_view()),
]
