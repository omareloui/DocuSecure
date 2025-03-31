from django.contrib.auth.models import User
from django.test import Client, TestCase
from docs.models import Doc
from elasticsearch_dsl import Q
from search.documents import DocDocument


class SearchTestCase(TestCase):
    def setUp(self):
        self.c = Client()

        user = User.objects.create_superuser(username="omareloui", password="123456")
        self.c.force_login(user)

    def test_creating_elastic_document_on_creating_document(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            self.c.post("/upload", {"file": fp})

        _q = Q("term", filename=filename)
        docs = DocDocument.search().query(_q).execute()
        self.assertIsNotNone(docs)
        self.assertGreater(len(docs), 0)

    def test_on_deleting_the_document_is_deleted(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            self.c.post("/upload", {"file": fp})

        _q = Q("term", filename=filename)
        docs = DocDocument.search().query(_q).execute()
        self.assertIsNotNone(docs)
        self.assertEqual(len(docs), 1)

        created_doc = Doc.objects.get(filename=filename)

        self.assertIsNotNone(created_doc)
        created_doc.delete()

        docs_after_deletion = DocDocument.search().query(_q).execute()
        self.assertEqual(len(docs_after_deletion), 0)
