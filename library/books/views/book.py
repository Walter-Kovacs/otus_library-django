from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    ListView,
)
from django.views.generic.edit import FormView

from books.forms import GetBookForm, ReturnBookForm
from books.models import Book
from users.models import Reader


class BookListView(ListView):
    model = Book
    template_name = 'book/list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/details.html'
    context_object_name = 'book'


class GetBookView(LoginRequiredMixin, DetailView, FormView):
    model = Book
    context_object_name = 'book'
    form_class = GetBookForm
    template_name = 'book/get.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            book = self.get_object()
            if book not in reader.books.all() and book.amount > 0:
                reader.books.add(book)
                reader.save()
                book.amount -= 1
                book.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()  # otherwise the object is missing
        return super().form_invalid(form)


class ReturnBookView(LoginRequiredMixin, DetailView, FormView):
    model = Book
    context_object_name = 'book'
    form_class = ReturnBookForm
    template_name = 'book/return.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            book = self.get_object()
            reader_books = reader.books
            if book in reader_books.all():
                reader_books.remove(book)
                reader.save()
                book.amount += 1
                book.save()

        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()  # otherwise the object is missing
        return super().form_invalid(form)