from django.test import TestCase
from faker import Faker

from books.models import (
    Genre,
)


class GenreViewContext(TestCase):

    def setUp(self):
        faker = Faker()
        for name in faker.words(nb=6, unique=True):
            Genre.objects.create(name=name)

        self.genres = Genre.objects.all()

    def tearDown(self):
        Genre.objects.all().delete()

    def test_all_genres_in_list_view_context(self):
        response = self.client.get('/genres/')
        context_objects = response.context['object_list']
        self.assertEquals(list(self.genres), list(context_objects))
