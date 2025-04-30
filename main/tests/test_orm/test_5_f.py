from django.db.models import F, Q

from .base import BaseORMTestCase


class TestF(BaseORMTestCase):
    def test_f(self):
        # Получить список закладок, у которых url НЕ совпадает с названием (т.е. НЕ равны), используя Q() и F()
        bookmarks = ...  # TODO

        self.assertEquals(self.BOOKMARK_TITLES, list(bookmarks.values_list('title', flat=True)))
