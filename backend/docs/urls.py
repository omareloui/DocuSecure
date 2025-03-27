from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="docs"),
    path("upload", views.upload, name="upload_doc"),
]
