from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    UserPassesTestMixin,
)
from django.urls import reverse_lazy

from users.models import Reader


class AdminLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self):
        return '/admin/'


class ReaderLoginRequiredMixin(LoginRequiredMixin):

    def get_login_url(self):
        return reverse_lazy('reader-login')


class AdminPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        return self.request.user.is_superuser


class ReaderPassesTestMixin(UserPassesTestMixin):

    def test_func(self):
        user = self.request.user
        reader = Reader.objects.filter(user__id=user.id).first()
        return reader is not None
