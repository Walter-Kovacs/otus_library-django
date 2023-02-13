from django.views.generic import ListView

from books.models import BookRequest
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class BookRequestListView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, ListView):
    model = BookRequest
    template_name = 'bookrequest/list.html'
    context_object_name = 'requests'
