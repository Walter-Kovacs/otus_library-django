from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)
from django.views.generic.edit import FormView

from books.forms import (
    LendBookForm,
    RequestBookForm,
    ReturnBookForm,
)
from books.models import (
    Book,
    BookCopy,
    BookRequest,
)
from users.models import Reader
from users.views.mixins import (
    LibrarianLoginRequiredMixin, LibrarianPassesTestMixin,
    ReaderLoginRequiredMixin, ReaderPassesTestMixin,
)


class BookListView(ListView):
    model = Book
    template_name = 'book/list.html'
    context_object_name = 'books'


class BookDetailView(DetailView):
    model = Book
    template_name = 'book/details.html'
    context_object_name = 'book'


class BookCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = Book
    fields = '__all__'
    template_name = 'book/form.html'
    success_url = reverse_lazy('book-list')


class BookUpdateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, UpdateView):
    model = Book
    fields = '__all__'
    template_name = 'book/form.html'
    success_url = reverse_lazy('book-list')


class BookDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = Book
    template_name = 'book/delete.html'
    success_url = reverse_lazy('book-list')


class RequestBookView(ReaderLoginRequiredMixin, ReaderPassesTestMixin, DetailView, FormView):
    model = Book
    context_object_name = 'book'
    form_class = RequestBookForm
    template_name = 'book/request.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            book = self.get_object()
            book_request = book.bookrequest_set.filter(reader=reader).first()
            if book_request is None:
                BookRequest.objects.create(book=book, reader=reader)

        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()  # otherwise the object is missing
        return super().form_invalid(form)


class LendBookView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DetailView, FormView):
    model = BookRequest
    context_object_name = 'request'
    form_class = LendBookForm
    template_name = 'book/lend.html'
    success_url = '/'

    def get_form(self, form_class=None):
        book_request = self.get_object()
        form = super().get_form(form_class)
        form.fields['inventory_number'].queryset = BookCopy.objects.filter(book=book_request.book, reader__isnull=False)
        return form

    def form_valid(self, form):
        book_request = self.get_object()
        # TODO: set reader and current date to book copy
        print(book_request)

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
