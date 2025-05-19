from .base import BaseORMTestCase

from ...models import Bookmark, Group
class TestBulkOperations(BaseORMTestCase):
    def test_bulk_create(self):
        # Создать группы из данных new_groups_data с помощью bulk_create
        new_groups_data = [
            ('Картинки', 10),
            ('Нейросети онлайн', 12),
            ('Идеи для творчества', 6),
        ]

        create_groups =[
            Group(name=name, order=order) for name, order in new_groups_data
        ]
        Group.objects.bulk_create(create_groups)
        # Проверим на существование новые группы
        for group_name, group_order in new_groups_data:
            self.assertTrue(Group.objects.filter(name=group_name, order=group_order).exists())

    def test_bulk_update(self):
        # Почистить данные закладок:
        # - удалить get-параметры из URL,
        # - сократить названия до 30 симв. макс.,
        # - написать дефолтное описание, если его нет.

        # Получить список всех закладок, подгрузив в тот же запрос связанные группы
        # Можно выбрать только те закладки, которые нуждаются в обновлении
        bookmarks = Bookmark.objects.select_related('group').all()
        bookmarks_to_update = []

        for bookmark in bookmarks:
            fields_changed = False

            if '?' in bookmark.url:
                #Эту строку мне самозаполнение подсказал, но как я понял, тут просто избавляемся от всего, что за ?
                changed_url = bookmark.url.split('?')[0]
                if changed_url != bookmark.url:
                    bookmarks.url = changed_url
                    fields_changed = True

                if len(bookmark.title) > 30:
                    bookmark.title = bookmark.title[:30]
                    fields_changed = True

                if not bookmark.description and bookmark.group:
                    bookmark.description = f'Закладка группы "{bookmark.group.name}"'
                    fields_changed = True
            if fields_changed:
                bookmarks_to_update.append(bookmark)

        self.assertEquals(5, len(bookmarks_to_update))
        #Как я понял bulk сюда
        Bookmark.objects.bulk_update(
            bookmarks_to_update,
        )

        # Проверим на существование обновленные закладки
        self.assertTrue(Bookmark.objects.filter(title='Торт Наполеон в домашних ус...').exists())
        self.assertTrue(Bookmark.objects.filter(
            title='Три рецепта «Оливье»: класс...',
            description='Закладка из группы "Рецепты"',
        ).exists())
        self.assertTrue(Bookmark.objects.filter(title='Апероль шприц. Состав, пров...').exists())
        self.assertTrue(Bookmark.objects.filter(url='https://mail.google.com/mail/u/0/').exists())
        self.assertTrue(Bookmark.objects.filter(title='Обои флизелиновые Аспект Ру...').exists())
