from django.db.models import Q

from .base import BaseORMTestCase


class TestQ(BaseORMTestCase):
    def test_q_and(self):
        # Получить закладку, у которой название и описание начинаются с 'Торт', используя Q()
        bookmark = ...  # TODO

        self.assertEquals(
            'https://www.gastronom.ru/recipe/15617/tort-napoleon-v-domashnih-uslovijah',
            bookmark.url
        )

    def test_q_or(self):
        # Получить названия закладок, у которых название начинается с 'Торт' ИЛИ и описание содержит 'рецепт'
        bookmark_titles = ...  # TODO

        self.assertIn(
            'Торт Наполеон в домашних условиях, пошаговый рецепт с фото на 382 ккал',
            bookmark_titles
        )
        self.assertIn(
            'Три рецепта «Оливье»: классический, советский и современный - РИА Новости, 11.12.2019',
            bookmark_titles
        )

    def test_q_not(self):
        # Получить названия закладок, в которых нет буквы 'а'
        bookmark_titles = ...  # TODO

        self.assertIn('Моё обучение – Stepik', bookmark_titles)
        self.assertIn('Gmail', bookmark_titles)
