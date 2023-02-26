from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, resolve_url
from django.urls import reverse_lazy
from django.views.generic import (
    DetailView,
    FormView,
    TemplateView,
)

from users.forms import ReaderRegistrationForm
from users.models import Reader
from users.views.mixins import (
    LibrarianLoginRequiredMixin,
    LibrarianPassesTestMixin,
    ReaderLoginRequiredMixin,
    ReaderPassesTestMixin,
)


class ReaderCreateView(FormView):
    form_class = ReaderRegistrationForm
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

        reader = Reader(
            user=user,
            address=form.data['address'],
            phone=form.data['phone'],
        )
        reader.save()

        return super().form_valid(form)


class ReaderLoginView(LoginView):
    template_name = 'reader/login.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_not_reader = False

    def form_valid(self, form):
        user = form.get_user()
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            return super().form_valid(form)
        else:
            self.is_not_reader = True
            return super().form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.is_not_reader:
            context['is_not_reader'] = True
            self.is_not_reader = False

        return context

    def get_default_redirect_url(self):
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return reverse_lazy('reader-profile')


class ReaderLogoutView(LogoutView):
    pass


class ReaderProfileView(ReaderLoginRequiredMixin, ReaderPassesTestMixin, TemplateView):
    template_name = 'reader/profile.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            return super().get(request, *args, **kwargs)
        else:
            return redirect('/')


class ReaderDetailView(LibrarianLoginRequiredMixin, LibrarianPassesTestMixin, DetailView):
    model = Reader
    template_name = 'reader/detail.html'
    context_object_name = 'reader'
