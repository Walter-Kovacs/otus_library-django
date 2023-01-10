from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    ListView,
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
