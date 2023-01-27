from django.test import TestCase
from faker import Faker

from books.models import (
    Genre,
)


class TestGenreModel(TestCase):

    def setUp(self) -> None:
        faker = Faker()
        genre_names = faker.words(nb=13, unique=True)
        for name in genre_names:
            Genre.objects.create(name=name)

    def tearDown(self) -> None:
        Genre.objects.all().delete()

    def test_str(self):
        genres = Genre.objects.all()
        for genre in genres:
            self.assertEqual(str(genre), genre.name)

    def test_ordering(self):
        genres = Genre.objects.all()
        genre_names = [g.name for g in genres]
        sorted_genre_names = sorted(genre_names)
        self.assertListEqual(sorted_genre_names, genre_names)
