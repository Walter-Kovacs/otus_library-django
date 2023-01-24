from django.test import TestCase
from mixer.backend.django import mixer

from books.models import BookCopy
from users.models import Reader


class TestBookCopyModel(TestCase):
    number_of_storage_copies = 3
    number_of_lend_copies = 2

    def setUp(self) -> None:
        self.reader = mixer.blend(Reader)
        mixer.cycle(TestBookCopyModel.number_of_storage_copies).blend(BookCopy, reader=None)
        mixer.cycle(TestBookCopyModel.number_of_lend_copies).blend(BookCopy, reader=self.reader)

    def tearDown(self) -> None:
        BookCopy.objects.all().delete()
        Reader.objects.all().delete()

    def test_number_of_all_copies(self):
        self.assertEquals(
            BookCopy.number_all(),
            TestBookCopyModel.number_of_storage_copies + TestBookCopyModel.number_of_lend_copies
        )

    def test_number_of_storage_copies(self):
        self.assertEquals(BookCopy.number_in_storage(), TestBookCopyModel.number_of_storage_copies)

    def test_number_of_lent_copies(self):
        self.assertEquals(BookCopy.number_lend(), TestBookCopyModel.number_of_lend_copies)

    def test_storage_copies(self):
        copies = BookCopy.objects.filter(reader__isnull=True)
        self.assertListEqual(
            list(copies),
            list(BookCopy.storage_copies())
        )

    def test_lend_copies(self):
        copies = BookCopy.objects.filter(reader__isnull=False)
        self.assertListEqual(
            list(copies),
            list(BookCopy.lend_copies())
        )
