from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    ListView,
    UpdateView,
)

from users.forms import (
    LibrarianRegistrationForm,
    RegisterLibrarianForm,
)
from users.models import Librarian
from users.views.mixins import AdminLoginRequiredMixin, AdminPassesTestMixin


class LibrarianCreateView(FormView):
    form_class = LibrarianRegistrationForm
    template_name = 'common/registration.html'
    success_url = '/'

    def form_valid(self, form):
        user = User(
            username=form.data['username'],
            first_name=form.data['first_name'],
            last_name=form.data['last_name'],
        )
        user.set_password(form.data['password1'])
        user.save()

        librarian = Librarian(
            user=user,
            address=form.data['address'],
            phone=form.data['phone'],
        )
        librarian.save()

        return super().form_valid(form)


class NewLibrarianListView(AdminLoginRequiredMixin, AdminPassesTestMixin, ListView):

    model = Librarian
    template_name = 'librarian/list_new.html'
    context_object_name = 'librarians'

    def get_queryset(self):
        # librarian is not in Library staff yet <=> staff_number = Null
        return Librarian.objects.filter(staff_number__isnull=True)


class RegisterLibrarian(AdminLoginRequiredMixin, AdminPassesTestMixin, UpdateView):
    model = Librarian
    form_class = RegisterLibrarianForm
    template_name = 'librarian/register.html'
    context_object_name = 'librarian'
    success_url = reverse_lazy('new-librarian-list')

    def get(self, request, *args, **kwargs):
        librarian = self.get_object()
        if librarian.is_active:
            return redirect('/')

        return super().get(request, *args, **kwargs)


class LibrarianListView(AdminLoginRequiredMixin, AdminPassesTestMixin, ListView):
    model = Librarian
    template_name = 'librarian/list.html'
    context_object_name = 'librarians'


class LibrarianLoginView(LoginView):
    template_name = 'librarian/login.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_not_staff = False

    def form_valid(self, form):
        user = form.get_user()
        librarian = Librarian.objects.filter(user__id=user.id).first()
        if librarian is not None and librarian.is_active:
            return super().form_valid(form)
        else:
            self.is_not_staff = True
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_not_staff:
            context['is_not_staff'] = True
            self.is_not_staff = False

        return context

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return reverse_lazy('bookrequest-list')


class LibrarianLogoutView(LogoutView):
    pass
