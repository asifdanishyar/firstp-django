from django.test import TestCase
from .models import Item


# Create your tests here.
class TestViews(TestCase):
    def test_get_todo_list(self):
        respons = self.client.get('/')
        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, 'todo/todo_list.html')

    def test_get_add_item_page(self):
        respons = self.client.get('/add')
        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, 'todo/add_item.html')

    def test_get_edit_item_page(self):
        item = Item.objects.create(name='Test Todo Item', done=False)
        respons = self.client.get(f'/edit/{item.id}')
        self.assertEqual(respons.status_code, 200)
        self.assertTemplateUsed(respons, 'todo/edit_item.html')

    def test_can_add_item(self):
        respons = self.client.post('/add', {'name': 'Test Added Item'})
        self.assertRedirects(respons, '/')

    def test_can_delete_item(self):
        item = Item.objects.create(name='Test Todo Item', done=False)
        respons = self.client.get(f'/delete/{item.id}')
        self.assertRedirects(respons, '/')
        existing_items = Item.objects.filter(id=item.id)
        self.assertEqual(len(existing_items), 0)

    def test_toggle_item(self):
        item = Item.objects.create(name='Test Todo Item', done=True)
        respons = self.client.get(f'/toggle/{item.id}')
        self.assertRedirects(respons, '/')
        updated_item = Item.objects.get(id=item.id)
        self.assertFalse(updated_item.done)
