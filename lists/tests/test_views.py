from django.test import TestCase
from django.utils.html import escape

# from django.urls import resolve
# from django.http import HttpRequest

# from .views import home_page
from ..models import Item, List


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')


class ListViewTest(TestCase):
    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item 1", list=correct_list)
        Item.objects.create(text="item 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="Other item 1", list=other_list)
        Item.objects.create(text="Other item 2", list=other_list)

        response = self.client.get('/lists/' + str(correct_list.id) + '/')
        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")
        self.assertNotContains(response, "Other item 1")
        self.assertNotContains(response, "Other item 2")

    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/' + str(list_.id) + '/')
        self.assertTemplateUsed(response, "list.html")

    def test_passes_context_list_to_templates(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/' + str(correct_list.id) + '/')
        self.assertEqual(response.context['list'], correct_list)

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/' + str(correct_list.id) + '/',
                         data={'item_text': "A new item for an existing list"})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post(('/lists/' +
                                     str(correct_list.id) + '/'),
                                    data={'item_text':
                                          'A new item for an existing list'})

        self.assertRedirects(response, '/lists/' + str(correct_list.id) + '/')


class NewListTest(TestCase):

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'item_text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_validation_errors_are_sent_back_to_home_page_template(self):
        response = self.client.post('/lists/new', data={"item_text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")
        expected_error = escape("You can't have an empty list item")
        self.assertContains(response, expected_error)

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={"item_text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={"item_text": "A new list item"})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/' + str(new_list.id) + '/')
