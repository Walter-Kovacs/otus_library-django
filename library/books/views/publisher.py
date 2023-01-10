from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    ListView,
    DeleteView,
    DetailView,
    UpdateView,
)

from books.models import Publisher
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class PublisherListView(ListView):
    model = Publisher
    template_name = 'publisher/list.html'
    context_object_name = 'publishers'


class PublisherDetailView(DetailView):
    model = Publisher
    template_name = 'publisher/details.html'
    context_object_name = 'publisher'


class PublisherCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = Publisher
    template_name = 'publisher/create.html'
    fields = '__all__'
    success_url = reverse_lazy('publisher-list')


class PublisherUpdateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, UpdateView):
    model = Publisher
    template_name = 'publisher/update.html'
    context_object_name = 'publisher'
    fields = '__all__'
    success_url = reverse_lazy('publisher-list')


class PublisherDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = Publisher
    template_name = 'publisher/delete.html'
    context_object_name = 'publisher'
    success_url = reverse_lazy('publisher-list')
