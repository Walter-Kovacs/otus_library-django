from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from books.forms import WrittenWorkForm
from books.models import (
    Genre,
    WrittenWork, Author,
)
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
)


class WrittenWorkListView(ListView):
    model = WrittenWork
    template_name = 'work/list.html'
    context_object_name = 'works'


class WrittenWorkDetailView(DetailView):
    model = WrittenWork
    template_name = 'work/details.html'
    context_object_name = 'work'


class WrittenWorkCreateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, CreateView):
    model = WrittenWork
    form_class = WrittenWorkForm
    template_name = 'work/form.html'
    success_url = reverse_lazy('work-list')

    def form_valid(self, form: WrittenWorkForm):
        work = WrittenWork.objects.create(
            title=form.title,
            genre=form.genre_object,
            description=form.description
        )

        work.author_set.add(*form.authors_ids)

        return super().form_valid(form)


class WrittenWorkUpdateView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, UpdateView):
    model = WrittenWork
    form_class = WrittenWorkForm
    template_name = 'work/form.html'
    success_url = reverse_lazy('work-list')

    def form_valid(self, form: WrittenWorkForm):
        work = self.get_object()
        work.author_set.clear()
        work.author_set.add(*form.authors_ids)

        return super().form_valid(form)


class WrittenWorkDeleteView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DeleteView):
    model = WrittenWork
    template_name = 'work/delete.html'
    context_object_name = 'work'
    success_url = reverse_lazy('work-list')
