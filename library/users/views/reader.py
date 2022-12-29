from django.contrib.auth.models import User
from django.views.generic.base import TemplateResponseMixin
from django.views.generic.edit import (
    FormMixin,
    ProcessFormView,
)

from users.forms import ReaderRegistrationForm
from users.models import Reader


class ReaderCreateView(TemplateResponseMixin, FormMixin, ProcessFormView):
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
