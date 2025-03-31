from os import path

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import Client, TestCase
from docs.models import Doc


class DocTestCase(TestCase):
    def setUp(self):
        self.c = Client()

        user = User.objects.create_superuser(username="omareloui", password="123456")
        self.c.force_login(user)

    def test_creating_document(self):
        with open("manage.py", "rb") as fp:
            res = self.c.post("/upload", {"file": fp})
            self.assertEqual(res.status_code, 302)
            self.assertEqual(res.headers.get("Location"), "/")

        doc = Doc.objects.get(filename="manage.py")
        self.assertIsNotNone(doc)
        doc.delete()

    def test_deleting_document(self):
        with open("manage.py", "rb") as fp:
            self.c.post("/upload", {"file": fp})

        doc = Doc.objects.get(filename="manage.py")
        self.assertIsNotNone(doc)
        doc.delete()

        with self.assertRaises(ObjectDoesNotExist):
            Doc.objects.get(filename="manage.py")

    def test_file_deletion_after_deleting_document(self):
        with open("manage.py", "rb") as fp:
            self.c.post("/upload", {"file": fp})

        doc = Doc.objects.get(filename="manage.py")
        self.assertIsNotNone(doc)
        doc.delete()

        self.assertFalse(path.isfile(doc.path))
