from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import redirect, render

from .form import LoginForm, RegisterForm, UplaodDocumentForm
from .models import Doc


def index(request):
    docs = Doc.objects.all()
    ctx = {"docs": docs}
    return render(request, "docs/index.html", ctx)


@login_required
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


def login_view(request):
    ctx = {}
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                next_url = (
                    request.POST.get("next") or request.GET.get("next") or "/docs"
                )
                return redirect(next_url)
            else:
                ctx["error"] = "Invaid Credentials!"
                ctx["form"] = form
                return render(request, "auth/login.html", ctx)

    ctx["form"] = LoginForm()
    return render(request, "auth/login.html", ctx)


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("/")
