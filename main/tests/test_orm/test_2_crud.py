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
        Bookmark.objects.create(url=url, title=title)

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_create_by_save(self):
        url = 'https://test1.com'
        title = 'Пример закладки 2'

        # Создать закладку с помощью метода save
        book = Bookmark(url=url, title=title)
        book.save()

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_create_by_save_fill_properties(self):
        url = 'https://test1.com'
        title = 'Пример закладки 3'

        # Создать закладку
        bookmark = Bookmark()
        bookmark.url = url
        bookmark.title = title
        bookmark.save()

        # Получим по полю url, сравним title
        bookmark = Bookmark.objects.get(url=url)
        self.assertEquals(title, bookmark.title)

    def test_update_fill_properties(self):
        # Обновить поле title закладки
        title = "Тест"
        self.bookmark.title = title

        # Подтянем обновленную модель из БД
        self.bookmark.refresh_from_db()

        # Сравним title
        self.assertEquals(title, self.bookmark.title)

    def test_update_by_method(self):
        # Всем группам задать order=0
        Group.objects.update(order=0)

        # Проверим, что у каждой группы order=0
        all_groups = Group.objects.all()

        for group in all_groups:
            self.assertEquals(0, group.order)

    def test_delete(self):
        # Удалить закладку и группу. Тут необходимо, чтобы было реализовано "мягкое удаление"
        self.bookmark.delete()
        self.group.delete()

        # Подтянем обновленную модель из БД
        self.bookmark.refresh_from_db()

        # Проверим, что у закладки заполнилось поле deleted
        self.assertIsNotNone(self.bookmark.time_deleted)

        # Проверим, что группы больше нет
        with self.assertRaises(Group.DoesNotExist):
            self.group.refresh_from_db()
