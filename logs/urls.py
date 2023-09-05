from django.urls import path

from .views import FileUploadView, StatusCodeList

urlpatterns = [
    path('upload', FileUploadView.as_view(), name='upload'),
    path('', StatusCodeList.as_view(), name='status_code')
]
