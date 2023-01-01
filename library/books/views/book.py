from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (
    DetailView,
    ListView,
)
from django.views.generic.edit import FormView

from books.forms import GetBookForm
from books.models import Book


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
    success_url = '/'

    def form_valid(self, form):
        print('*' * 50, "form_valid", '*' * 50)
        # TODO: book to user
        return super().form_valid(form)

    def form_invalid(self, form):
        print('*' * 50, "form_invalid", '*' * 50)
        self.object = self.get_object()  # otherwise the object is missing
        return super().form_invalid(form)

