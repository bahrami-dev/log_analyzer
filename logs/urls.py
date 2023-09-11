from django.urls import path

from .views import FileUploadView, Statistics


urlpatterns = [
    path('upload', FileUploadView.as_view(), name='upload'),
    path('<int:id>/statistics', Statistics.as_view(), name='statistics')
]
