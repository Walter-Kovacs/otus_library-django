from datetime import date

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
)
from books.models import (
    Book,
    BookCopy,
    BookRequest,
)
from users.models import (
    Librarian,
    Reader,
)
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
    context_object_name = 'book'

    def get_template_names(self):
        user = self.request.user
        librarian = Librarian.objects.filter(user__id=user.id).first()
        if librarian is not None:
            return ['book/details_for_librarian.html']
        else:
            return ['book/details.html']

    def get_context_data(self, **kwargs):
        book = self.get_object()
        context = super().get_context_data(**kwargs)
        all_copies = BookCopy.objects.filter(book=book)
        reader_copies = sorted(
            [copy for copy in all_copies if copy.reader is not None],
            key=lambda copy: copy.reader.user.first_name
        )
        context['all_copies'] = all_copies
        context['reader_copies'] = reader_copies
        return context


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.no_available_copies = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.no_available_copies:
            context['no_available_copies'] = True
            self.no_available_copies = False
        return context

    def form_valid(self, form):
        book = self.get_object()
        if BookCopy.number_in_storage(book.id) < 1:
            self.no_available_copies = True
            return self.form_invalid(form)

        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
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
    success_url = reverse_lazy('bookrequest-list')

    def get_form(self, form_class=None):
        book_request = self.get_object()
        form = super().get_form(form_class)
        form.fields['inventory_number'].queryset = BookCopy.objects.filter(book=book_request.book, reader__isnull=True)
        return form

    def form_valid(self, form):
        book_request = self.get_object()
        copy = BookCopy.objects.get(id=form.copy_id)
        copy.reader = book_request.reader
        copy.reader_date = date.today()
        copy.save()
        book_request.delete()

        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = self.get_object()  # otherwise the object is missing
        return super().form_invalid(form)
