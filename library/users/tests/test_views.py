from django.contrib.auth.models import User
from django.test import TestCase
from faker import Faker
from mixer.backend.django import mixer

from users.models import (
    Librarian,
    Reader,
)


class LibrarianViewContext(TestCase):
    admin_username = 'admin'
    admin_password = 'admin12345678'

    def setUp(self) -> None:
        faker = Faker()
        staff_nums = [faker.pystr(min_chars=8, max_chars=8) for i in range(4)]
        mixer.cycle(4).blend(Librarian, staff_number=(sn for sn in staff_nums))
        mixer.cycle(2).blend(Librarian, staff_number=None)

        User.objects.create_superuser(username=self.admin_username, password=self.admin_password)
        self.client.login(username=self.admin_username, password=self.admin_password)

    def tearDown(self) -> None:
        Librarian.objects.all().delete()
        User.objects.all().delete()

    def test_only_new_librarians_in_new_librarian_view_context(self):
        response = self.client.get('/users/librarians/new/')
        context_objects = response.context['librarians']
        new_librarians = Librarian.objects.filter(staff_number__isnull=True)
        self.assertEquals(list(new_librarians), list(context_objects))

    def test_all_librarians_in_librarian_list_view_context(self):
        response = self.client.get('/users/librarians/')
        context_objects = response.context['librarians']
        all_librarians = Librarian.objects.all()
        self.assertEquals(list(all_librarians), list(context_objects))
