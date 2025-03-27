from logging import getLogger

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods
from elasticsearch_dsl import Q

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
