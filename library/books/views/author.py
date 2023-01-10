from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from books.models import Author
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class AuthorListView(ListView):
    model = Author
    template_name = 'author/list.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author/details.html'
    context_object_name = 'author'


class AuthorCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = Author
    template_name = 'author/create.html'
    fields = (
        'name',
        'about',
    )
    success_url = reverse_lazy('author-list')


class AuthorUpdateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, UpdateView):
    model = Author
    template_name = 'author/update.html'
    context_object_name = 'author'
    fields = (
        'name',
        'about',
    )
    success_url = reverse_lazy('author-list')


class AuthorDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = Author
    template_name = 'author/delete.html'
    context_object_name = 'author'
    success_url = reverse_lazy('author-list')
