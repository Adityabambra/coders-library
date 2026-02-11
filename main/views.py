from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Book, ReadingHistory
from django.db.models import Q
from django.utils import timezone

def home(request):
    return render(request, "home.html")


def books(request):
    query = request.GET.get('q','')
    
    if query:
        books = Book.objects.filter(
            Q(title__icontains=query) | Q(author__icontains=query)
        )
    else:
        books = Book.objects.all()
    
    context =  {'books': books,'query':query}

    return render(request, 'books.html',context)


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    return render(request, "book_detail.html", {"book": book})


@login_required
def read_book(request, book_id):
    book = get_object_or_404(Book, id=book_id)

    # Update existing history OR create new one
    history, created = ReadingHistory.objects.update_or_create(
        user=request.user,
        book=book,
        defaults={'read_at': timezone.now()}
    )

    return redirect(book.pdf_file.url)


@login_required
def history(request):
    records = ReadingHistory.objects.filter(user=request.user).order_by("-read_at")
    return render(request, "history.html", {"records": records})


# ---------- AUTH ----------

def sign_up(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        pass1 = request.POST.get("pass1", "")
        pass2 = request.POST.get("pass2", "")

        if not username or not pass1 or not pass2:
            return render(request, "sign_up.html", {"error": "All fields required"})

        if User.objects.filter(username=username).exists():
            return render(request, "sign_up.html", {"error": "Username already exists"})

        if pass1 != pass2:
            return render(request, "sign_up.html", {"error": "Passwords do not match"})

        user = User.objects.create_user(username=username, password=pass1)
        login(request, user)
        return redirect("home")

    return render(request, "sign_up.html")


def sign_in(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect("home")
        else:
            return render(request, "sign_in.html", {"error": "Invalid credentials"})

    return render(request, "sign_in.html")


def sign_out(request):
    logout(request)
    return redirect("home")
