from .base import BaseORMTestCase


class TestBulkOperations(BaseORMTestCase):
    def test_bulk_create(self):
        # Создать группы из данных new_groups_data с помощью bulk_create
        new_groups_data = [
            ('Картинки', 10),
            ('Нейросети онлайн', 12),
            ('Идеи для творчества', 6),
        ]

        # TODO ...
        ...
        ...

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
        bookmarks = ... # TODO
        bookmarks_to_update = []

        for bookmark in bookmarks:
            fields_changed = False

            # TODO ...
            ...
            ...

            if fields_changed:
                ...  # TODO

        self.assertEquals(5, len(bookmarks_to_update))

        ...  # TODO

        # Проверим на существование обновленные закладки
        self.assertTrue(Bookmark.objects.filter(title='Торт Наполеон в домашних ус...').exists())
        self.assertTrue(Bookmark.objects.filter(
            title='Три рецепта «Оливье»: класс...',
            description='Закладка из группы "Рецепты"',
        ).exists())
        self.assertTrue(Bookmark.objects.filter(title='Апероль шприц. Состав, пров...').exists())
        self.assertTrue(Bookmark.objects.filter(url='https://mail.google.com/mail/u/0/').exists())
        self.assertTrue(Bookmark.objects.filter(title='Обои флизелиновые Аспект Ру...').exists())
