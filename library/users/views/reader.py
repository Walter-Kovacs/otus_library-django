from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import (
    FormView,
    TemplateView,
)

from users.forms import ReaderRegistrationForm
from users.models import Reader
from users.views.mixins import ReaderLoginRequiredMixin, ReaderPassesTestMixin


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
    success_url = reverse_lazy('reader-profile')

    def form_valid(self, form):
        user = form.get_user()
        reader = Reader.objects.filter(user__id=user.id).first()
        if reader is not None:
            return super().form_valid(form)
        else:
            return super().form_invalid(form)


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
