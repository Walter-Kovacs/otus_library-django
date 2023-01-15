from django.views.generic import (
    ListView,
    DetailView,
)

from books.models import Publisher


class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher/list.html'
    context_object_name = 'publishers'


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'publisher/details.html'
    context_object_name = 'publisher'
