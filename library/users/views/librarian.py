from django.contrib.auth.models import User
from django.views.generic import FormView

from users.forms import LibrarianRegistrationForm
from users.models import Librarian


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
