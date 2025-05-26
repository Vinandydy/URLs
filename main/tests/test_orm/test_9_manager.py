from .base import BaseORMTestCase
from ...models import Bookmark


class TestManager(BaseORMTestCase):
    def test_without_deleted(self):
        # Удалить закладку с url 'https://ru.inshaker.com/cocktails/1098-aperol-shprits'
        bookmark = Bookmark.objects.get(url='https://ru.inshaker.com/cocktails/1098-aperol-shprits')
        bookmark.delete()

        # Получить все закладки, кроме удаленных, используя соответствующий метод менеджера
        bookmarks_without_deleted_titles = Bookmark.objects.without_deleted().values('title')

        self.assertNotIn(
            'Апероль шприц. Состав, проверенный рецепт и фото коктейля Апероль шприц — Inshaker',
            bookmarks_without_deleted_titles
        )
