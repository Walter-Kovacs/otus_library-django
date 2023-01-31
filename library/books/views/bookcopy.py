from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    FormView,
)

from books.forms import ReturnBookForm
from books.models import BookCopy
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class BookCopyCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = BookCopy
    fields = (
        'book',
        'inventory_number',
    )
    template_name = 'bookcopy/create.html'
    success_url = reverse_lazy('bookcopy-create')


class BookCopyReturnView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DetailView, FormView):
    model = BookCopy
    context_object_name = 'copy'
    form_class = ReturnBookForm
    template_name = 'bookcopy/return.html'
    success_url = reverse_lazy('book-list')

    def form_valid(self, form):
        copy = self.get_object()
        copy.reader = None
        copy.reader_date = None
        copy.save()

        return super().form_valid(form)
