from django.test import TestCase

from ...models import Bookmark, Group


class TestCrud(TestCase):
    group: Group
    bookmark: Bookmark

    def setUp(self):
        self.group = Group.objects.create(
            name='Разное',
            order=1,
        )

        self.bookmark = Bookmark.objects.create(
            url='https://test.com',
            title='Тест',
            description='Тест тест',
            group=self.group,
        )

    def test_create_by_method(self):
        url = 'https://test1.com'
        title = 'Пример закладки'

        # Создать закладку с помощью метода create
        ... # TODO

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_create_by_save(self):
        url = 'https://test1.com'
        title = 'Пример закладки 2'

        # Создать закладку с помощью метода save
        ... # TODO

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_create_by_save_fill_properties(self):
        url = 'https://test1.com'
        title = 'Пример закладки 3'

        # Создать закладку
        bookmark = Bookmark()
        bookmark.url = ...
        ...
        ...
        # TODO

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_update_fill_properties(self):
        # Обновить поле title закладки
        title = ...  # TODO
        self.bookmark.title = ...  # TODO

        # Подтянем обновленную модель из БД
        ...  # TODO

        # Сравним title
        self.assertEquals(title, self.bookmark.title)

    def test_update_by_method(self):
        # Всем группам задать order=0
        ...  # TODO

        # Проверим, что у каждой группы order=0
        all_groups = Group.objects.all()

        for group in all_groups:
            self.assertEquals(0, group.order)

    def test_delete(self):
        # Удалить закладку и группу. Тут необходимо, чтобы было реализовано "мягкое удаление"
        ...  # TODO
        ...  # TODO

        # Подтянем обновленную модель из БД
        ...  # TODO

        # Проверим, что у закладки заполнилось поле deleted
        self.assertIsNotNone(self.bookmark.time_deleted)

        # Проверим, что группы больше нет
        with self.assertRaises(Group.DoesNotExist):
            self.group.refresh_from_db()
