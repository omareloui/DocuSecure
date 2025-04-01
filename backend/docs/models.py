import os
from logging import getLogger

import magic
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import gettext_lazy as _

from .lib.parse_doc import FileParser, get_parser_from_mimetype

UPLOAD_TO = "uploads/%Y/%m/%d/"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doc(BaseModel):
    class DocStatus(models.TextChoices):
        PENDING = "PENDING", _("Pending Parsing")
        PARSED = "PARSED", _("Parsed")

    content = models.TextField()
    file = models.FileField(upload_to=UPLOAD_TO)
    filename = models.CharField(max_length=64)
    path = models.CharField(max_length=64)
    url = models.CharField(max_length=64)
    size = models.IntegerField()
    mimetype = models.CharField(max_length=64)

    classification = models.CharField(null=True, max_length=64)
    confidence = models.FloatField(default=0)

    # TODO: for now it'll be a comma separated list
    keywords = models.TextField(null=True)

    status = models.CharField(
        max_length=16,
        choices=DocStatus,
        default=DocStatus.PENDING,
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    _parser = None

    def delete(self, using=None, keep_parents=False):
        super().delete(using, keep_parents)
        try:
            os.unlink(self.path)
        except FileNotFoundError:
            logger = getLogger("loggers")
            logger.warning(
                {"message": "Couldn't find file to delete", "path": doc.path}
            )

    def get_metadata(self):
        return {
            "document_id": self.id,
            "title": self.filename,
            "author": self.owner.username,
            "date_created": self.created_at,
            "keywords": self.keywords and self.keywords.split(","),
        }

    def save_from_file_and_user(file, user):
        doc = Doc()
        doc.file = file
        doc.filename = file.name
        doc.size = file.size
        doc.owner = user
        doc.mimetype = file.content_type

        # To fail before saving the file and doc
        get_parser_from_mimetype(doc.mimetype)

        # We'll need to save before setting the path and url
        doc.save()

        doc.set_file_metadata()
        doc.set_content_from_file()
        doc.save()
        return doc

    def set_file_metadata(self):
        self.path = self.file.path
        self.url = self.file.url
        self.mimetype = magic.from_file(self.path, mime=True)

    def set_content_from_file(self):
        if not self._parser:
            self._parser = FileParser(get_parser_from_mimetype(self.mimetype))

        self.content = self._parser.parse(f"{settings.MEDIA_ROOT}/{self.file.name}")
        self.status = self.DocStatus.PARSED

    def __str__(self):
        return f"[{self.id}] <{self.mimetype}> {self.content}"
