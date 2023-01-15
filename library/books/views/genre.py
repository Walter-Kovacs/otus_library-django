from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from books.models import Genre
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class GenreListView(ListView):
    model = Genre
    template_name = 'genre/list.html'


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre/details.html'


class GenreCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = Genre
    template_name = 'genre/create.html'
    fields = '__all__'
    success_url = reverse_lazy('genre-list')


class GenreUpdateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, UpdateView):
    model = Genre
    template_name = 'genre/update.html'
    context_object_name = 'genre'
    fields = '__all__'
    success_url = reverse_lazy('genre-list')


class GenreDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = Genre
    template_name = 'genre/delete.html'
    context_object_name = 'genre'
    success_url = reverse_lazy('genre-list')
