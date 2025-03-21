from django.shortcuts import redirect, render

from .form import DocumentForm
from .models import Doc


def index(request):
    docs = Doc.objects.all()
    ctx = {"docs": docs}
    return render(request, "docs/index.html", ctx)


def create(request):
    ctx = {}
    if request.method == "POST":
        form = DocumentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/docs")
        else:
            ctx["form"] = DocumentForm(request.POST)
            return render(request, "docs/create.html", ctx)

    ctx["form"] = DocumentForm()
    return render(request, "docs/create.html", ctx)
