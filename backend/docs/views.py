from logging import getLogger

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_GET, require_http_methods, require_POST
from elasticsearch_dsl import Q

from search.documents import DocDocument

from .form import LoginForm, RegisterForm, SearchForm, UplaodDocumentForm
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


@require_http_methods(["GET", "POST"])
def register(request):
    ctx = {}
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(
                username=username, email=email, password=password
            )
            login(request, user)
            return redirect("/")
        else:
            ctx["form"] = RegisterForm(request.POST)
            return render(request, "auth/register.html", ctx)
    ctx["form"] = RegisterForm()
    return render(request, "auth/register.html", ctx)


@require_http_methods(["GET", "POST"])
def login_view(request):
    next_url = request.POST.get("next") or request.GET.get("next") or "docs"
    ctx = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_url)
            else:
                ctx["error"] = "Invaid Credentials!"
                ctx["form"] = form
                return render(request, "auth/login.html", ctx)

    ctx["form"] = LoginForm(initial={"next": next_url})
    return render(request, "auth/login.html", ctx)


@require_POST
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("/")
