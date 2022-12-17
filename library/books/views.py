from django.shortcuts import render

from books.models import Book


def welcome(request):
    books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'welcome.html', context=context)
