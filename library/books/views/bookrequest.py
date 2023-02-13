from django.urls import reverse_lazy
from django.views.generic import (
    DeleteView,
    ListView,
)

from books.models import BookRequest
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class BookRequestListView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, ListView):
    model = BookRequest
    template_name = 'bookrequest/list.html'
    context_object_name = 'requests'


class BookRequestDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = BookRequest
    template_name = 'bookrequest/delete.html'
    context_object_name = 'request'
    success_url = reverse_lazy('bookrequest-list')
