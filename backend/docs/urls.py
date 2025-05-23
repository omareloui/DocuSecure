from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="docs"),
    path("upload", views.upload, name="upload_doc"),
    path("bulk-upload", views.bulk_upload, name="bulk_upload_doc"),
    path("<int:id>/delete", views.delete, name="delete_doc"),
]
