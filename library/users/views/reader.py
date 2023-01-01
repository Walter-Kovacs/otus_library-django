from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import FormView

from users.forms import ReaderRegistrationForm
from users.models import Reader


class ReaderCreateView(FormView):
    form_class = ReaderRegistrationForm
    template_name = 'reader/registration.html'
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


class ReaderLogoutView(LogoutView):
    pass


class ReaderProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'reader/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        context['reader'] = reader
        return context
