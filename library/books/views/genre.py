from django.views.generic import (
    DetailView,
    ListView,
)

from books.models import Genre


class GenreListView(ListView):
    model = Genre
    template_name = 'genre/list.html'


class GenreDetailView(DetailView):
    model = Genre
    template_name = 'genre/details.html'
