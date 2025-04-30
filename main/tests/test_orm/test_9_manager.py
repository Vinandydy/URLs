from .base import BaseORMTestCase


class TestManager(BaseORMTestCase):
    def test_without_deleted(self):
        # Удалить закладку с url 'https://ru.inshaker.com/cocktails/1098-aperol-shprits'
        # TODO ...

        # Получить все закладки, кроме удаленных, используя соответствующий метод менеджера
        bookmarks_without_deleted_titles = ... # TODO

        self.assertNotIn(
            'Апероль шприц. Состав, проверенный рецепт и фото коктейля Апероль шприц — Inshaker',
            bookmarks_without_deleted_titles
        )
