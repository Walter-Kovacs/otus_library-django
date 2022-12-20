from django.views.generic import (
    DetailView,
    ListView,
)

from books.models import Author


class AuthorListView(ListView):
    model = Author
    template_name = 'author/list.html'
    context_object_name = 'authors'


class AuthorDetailView(DetailView):
    model = Author
    template_name = 'author/details.html'
    context_object_name = 'author'
