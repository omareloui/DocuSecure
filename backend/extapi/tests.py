from django.contrib.auth.models import User
from django.test import Client, TestCase
from docs.models import Doc
from extapi.views import metadata


class ExtApiTestCase(TestCase):
    def setUp(self):
        self.c = Client()

        user = User.objects.create_superuser(username="omareloui", password="123456")
        self.c.force_login(user)

    def test_creating_doc(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            res = self.c.post("/documents/", {"file": fp})
            self.assertEqual(res.status_code, 200)
            self.assertGreater(res.json()["document_id"], 0)

    def test_document_metadata(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            res = self.c.post("/documents/", {"file": fp})
            doc_id = res.json()["document_id"]

        res = self.c.get(f"/documents/{doc_id}/metadata")
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertGreater(json["document_id"], 0)
        self.assertIsNotNone(json["title"])
        self.assertIsNotNone(json["author"])
        self.assertIsNotNone(json["date_created"])

    def test_document_extract_metadata(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            res = self.c.post("/documents/", {"file": fp})
            doc_id = res.json()["document_id"]

        doc = Doc.objects.get(id=doc_id)

        res = self.c.post("/documents/metadata/extract", {"file_url": doc.url})
        self.assertEqual(res.status_code, 200)
        json = res.json()
        metadata = json["extracted_metadata"]
        self.assertEqual(json["status"], "PARSED")
        self.assertGreater(metadata["document_id"], 0)
        self.assertIsNotNone(metadata["title"])
        self.assertIsNotNone(metadata["author"])
        self.assertIsNotNone(metadata["date_created"])

    def test_document_classify(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            res = self.c.post("/documents/", {"file": fp})
            doc_id = res.json()["document_id"]

        doc = Doc.objects.get(id=doc_id)

        res = self.c.post("/documents/classify", {"file_url": doc.url})
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertEqual(json["status"], "PARSED")
        self.assertIsNotNone(json["classification"])
        self.assertGreater(json["confidence"], 0)

    def test_get_document_status(self):
        filename = "requirements.txt"
        with open(filename, "rb") as fp:
            res = self.c.post("/documents/", {"file": fp})
            doc_id = res.json()["document_id"]

        res = self.c.get(f"/documents/{doc_id}/status")
        self.assertEqual(res.status_code, 200)
        json = res.json()
        self.assertEqual(json["document_id"], doc_id)
        self.assertEqual(json["status"], "PARSED")
        self.assertIsNotNone(json["last_updated"])
