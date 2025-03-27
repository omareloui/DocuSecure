import os
from logging import getLogger

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from elasticsearch_dsl import Q

from docusecure import settings
from search.documents import DocDocument

from .form import SearchForm, UplaodDocumentForm
from .models import Doc


@require_GET
def index(request):
    q = request.GET.get("q")

    logger = getLogger("loggers")

    if q:
        _q = Q("fuzzy", content={"value": q, "fuzziness": 1})
        docs = DocDocument.search().query(_q).execute()
    else:
        docs = Doc.objects.all()
    logger.info({"query": q, "docs_count": len(docs)})
    ctx = {"docs": docs, "q": q, "search_form": SearchForm(request.GET)}
    return render(request, "docs/index.html", ctx)


@require_http_methods(["GET", "POST"])
@login_required()
@permission_required("docs.add_doc", raise_exception=True)
def upload(request):
    ctx = {}
    if request.method == "POST":
        doc = Doc(owner=request.user, mimetype="text/plain")
        form = UplaodDocumentForm(
            request.POST,
            request.FILES,
            instance=doc,
        )
        if form.is_valid():
            form.save()
            doc.set_content_from_file()
            return redirect("/")
        else:
            ctx["form"] = UplaodDocumentForm(request.POST, request.FILES)
            return render(request, "docs/upload.html", ctx)

    ctx["form"] = UplaodDocumentForm()
    return render(request, "docs/upload.html", ctx)


@require_POST
@login_required()
@permission_required("docs.delete_doc", raise_exception=True)
def delete(request, id):
    logger = getLogger("loggers")
    doc = Doc.objects.get(id=id)
    logger.info(
        {"id": id, "action": "DELETE", "subject": "docs", "doc": doc, "file": doc.file}
    )

    _path = doc.file.path

    try:
        os.unlink(_path)
    except FileNotFoundError:
        logger.warning({"message": "Couldn't find file to delete", "path": _path})
        pass

    doc.delete()
    return redirect("docs")
