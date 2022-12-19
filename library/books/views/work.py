from django.views.generic import (
    DetailView,
    ListView,
)

from books.models import WrittenWork


class WrittenWorkListView(ListView):
    model = WrittenWork
    template_name = 'work/list.html'
    context_object_name = 'works'


class WrittenWorkDetailView(DetailView):
    model = WrittenWork
    template_name = 'work/details.html'
    context_object_name = 'work'
