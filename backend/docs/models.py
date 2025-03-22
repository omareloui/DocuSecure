from django.contrib.auth.models import User
from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Doc(BaseModel):
    title = models.CharField(max_length=64)
    content = models.TextField()
    # owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title} => {self.content} - {self.owner}"
