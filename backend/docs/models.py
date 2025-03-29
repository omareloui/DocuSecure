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

    def get_metadata(self):
        return {
            "document_id": self.id,
            "title": self.filename,
            "author": self.owner.username,
            "date_created": self.created_at,
            "keywords": self.keywords and self.keywords.split(","),
        }

    def set_file_metadata(self):
        self.path = self.file.path
        self.url = self.file.url

    def set_content_from_file(self):
        if not self._parser:
            self._parser = FileParser(get_parser_from_mimetype(self.mimetype))

        dir = f"{settings.MEDIA_ROOT}"
        self.content = self._parser.parse(f"{dir}/{self.file.name}")
        self.status = self.DocStatus.PARSED

    def __str__(self):
        return f"[{self.id}] <{self.mimetype}> {self.content}"
