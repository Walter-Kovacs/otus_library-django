from django.contrib.auth.models import User
from django.test import TestCase

from .models import Reader


class TestReader(TestCase):

    def test_get_reader_from_user(self):
        user = User.objects.create_user(username='Jack', password='jack12345678')
        Reader.objects.create(user=user, address='Izhevsk', phone='1234567890')

        reader = Reader.objects.filter(user__id=user.id).first()
        print("reader:", reader.user.username, reader.address, reader.phone)

        none_reader = Reader.objects.filter(user__id=user.id + 1).first()
        print("none_reader: ", none_reader)
