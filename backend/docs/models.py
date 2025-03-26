from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

from .lib.parse_doc import FileParser, get_parser_from_mimetype

UPLOAD_TO = "uploads/%Y/%m/%d/"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doc(BaseModel):
    content = models.TextField()
    file = models.FileField(upload_to=UPLOAD_TO)
    mimetype = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    _parser = None

    def set_content_from_file(self):
        if not self._parser:
            self._parser = FileParser(get_parser_from_mimetype(self.mimetype))

        dir = f"{settings.MEDIA_ROOT}"
        self.content = self._parser.parse(f"{dir}/{self.file.name}")
        self.save()

    def __str__(self):
        return f"[{self.id}] <{self.mimetype}> {self.content}"
