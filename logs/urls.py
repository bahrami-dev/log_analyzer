from django.urls import path

from .views import FileUploadView, Statistics


urlpatterns = [
    path('', FileUploadView.as_view(), name='logs'),
    path('/<int:pk>', FileUploadView.as_view(), name='update'),
    path('/<int:id>/statistics', Statistics.as_view(), name='statistics')
]
