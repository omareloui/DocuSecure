from django.urls import path

from . import views

urlpatterns = [
    path("documents/", views.create_document, name="create_document"),
    path("documents/<int:document_id>/metadata", views.metadata, name="metadata"),
    path(
        "documents/metadata/extract",
        views.extract_metadata,
        name="extract_document_metadata",
    ),
    path(
        "documents/classify",
        views.classify,
        name="classify_document",
    ),
    path(
        "documents/<int:document_id>/status",
        views.status,
        name="document_status",
    ),
]
