from django.db.models import Q

from .base import BaseORMTestCase
from ...models import Bookmark


class TestQ(BaseORMTestCase):
    #Все же я немного путаюсь с тем, где следует values_list возвращать, а где first
    def test_q_and(self):
        # Получить закладку, у которой название и описание начинаются с 'Торт', используя Q()
        bookmark = Bookmark.objects.filter(
            Q(title__startswith='Торт') & Q(description__startswith='Торт')
        ).first()

        self.assertEquals(
            'https://www.gastronom.ru/recipe/15617/tort-napoleon-v-domashnih-uslovijah',
            bookmark.url
        )

    #Было бы здесь более правильно использовать icontains?
    def test_q_or(self):
        # Получить названия закладок, у которых название начинается с 'Торт' ИЛИ и описание содержит 'рецепт'
        bookmark_titles = Bookmark.objects.filter(
            Q(title__startswith='Торт') | Q(title__contains='рецепт')
        ).values_list('title', flat=True)

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
        bookmark_titles = Bookmark.objects.filter(
            ~Q(title__contains='а')
        ).values_list('title', flat=True)

        self.assertIn('Моё обучение – Stepik', bookmark_titles)
        self.assertIn('Gmail', bookmark_titles)
