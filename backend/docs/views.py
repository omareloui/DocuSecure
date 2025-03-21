from django.shortcuts import render

from .models import Doc


def index(request):
    docs = Doc.objects.all()
    ctx = {"docs": docs}
    return render(request, "docs/index.html", ctx)
