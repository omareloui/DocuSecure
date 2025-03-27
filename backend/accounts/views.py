from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods, require_POST

from accounts.forms import LoginForm, RegisterForm


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
            return render(request, "accounts/register.html", ctx)
    ctx["form"] = RegisterForm()
    return render(request, "accounts/register.html", ctx)


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
                return render(request, "accounts/login.html", ctx)

    ctx["form"] = LoginForm(initial={"next": next_url})
    return render(request, "accounts/login.html", ctx)


@require_POST
def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("/")
