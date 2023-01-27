from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
)

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
