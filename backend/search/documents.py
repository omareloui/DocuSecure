from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from docs.models import Doc


@registry.register_document
class DocDocument(Document):
    owner = fields.ObjectField(
        properties={
            "id": fields.IntegerField(),
            "first_name": fields.TextField(),
            "last_name": fields.TextField(),
            "username": fields.TextField(),
            "email": fields.TextField(),
        }
    )

    class Index:
        name = "doc"
        settings = {"number_of_shards": 1, "number_of_replicas": 0}

    class Django:
        model = Doc

        fields = [
            "id",
            "content",
            "file",
            "mimetype",
        ]
