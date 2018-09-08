"""
WHAT TO WRITE IN VIEWS TESTS:
------------------------------
1- USE THE DJANGO TEST CLIENT
2- CHECK THE TEMPLATE USED AND THEN CHECK EACH ITEM
   IN CONTEXT
3- CHECK THAT ANY OBJECTS ARE THE RIGHT ONES, OR
   QUERYSETS HAVE THE CORRECT ITEMS
4- CHECK THAT ANY FORMS ARE OF THE RIGHT CLASS
5- THINK ABOUT TESTING TEMPLATE LOGIC: ANY FOR/IF
   MIGHT DESERVE A MINIMAL TEST
6- FOR POST REQUESTS, MAKE SURE YOU TEST FOR BOTH
   VALID AND INVALID CASES
7- CHECK THAT FORM IS RENDERED AND ERRORS ARE DISPLAYED
"""
from django.test import TestCase
from django.utils.html import escape

from ..models import Item, List
from ..forms import (ItemForm, EMPTY_ITEM_ERROR,
                     ExistingListItemForm, DUPLICATE_ITEM_ERROR)


class HomePageTest(TestCase):
    def test_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_uses_item_form(self):
        response = self.client.get('/')
        self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

    def test_uses_list_template(self):
        list_ = List.objects.create()
        """
        USE THE DJANGO TEST CLIENT
        """
        response = self.client.get('/lists/' + str(list_.id) + '/')
        """
        CHECK THE TEMPLATE USED AND THEN CHECK EACH ITEM
        IN CONTEXT
        """
        self.assertTemplateUsed(response, "list.html")

    def test_passes_context_list_to_templates(self):
        List.objects.create()
        correct_list = List.objects.create()

        response = self.client.get('/lists/' + str(correct_list.id) + '/')
        """
        CHECK THAT ANY OBJECTS ARE THE RIGHT ONES, OR
        QUERYSETS HAVE THE CORRECT ITEMS
        """
        self.assertEqual(response.context['list'], correct_list)

    def test_displays_item_form(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/' + str(list_.id) + '/')
        """
        CHECK THAT ANY FORMS ARE OF THE RIGHT CLASS
        """
        self.assertIsInstance(response.context['form'], ExistingListItemForm)
        self.assertContains(response, 'name="text"')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text="item 1", list=correct_list)
        Item.objects.create(text="item 2", list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text="Other item 1", list=other_list)
        Item.objects.create(text="Other item 2", list=other_list)
        """
        THINK ABOUT TESTING TEMPLATE LOGIC: ANY FOR/IF
        MIGHT DESERVE A MINIMAL TEST
        """
        response = self.client.get('/lists/' + str(correct_list.id) + '/')
        self.assertContains(response, "item 1")
        self.assertContains(response, "item 2")
        self.assertNotContains(response, "Other item 1")
        self.assertNotContains(response, "Other item 2")

    """
    FOR POST REQUESTS, MAKE SURE YOU TEST FOR BOTH
    VALID AND INVALID CASES
    """

    def test_can_save_a_POST_request_to_an_existing_list(self):
        List.objects.create()
        correct_list = List.objects.create()

        self.client.post('/lists/' + str(correct_list.id) + '/',
                         data={'text': "A new item for an existing list"})
        self.assertEqual(Item.objects.count(), 1)

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')
        self.assertEqual(new_item.list, correct_list)

    def test_POST_redirects_to_list_view(self):
        correct_list = List.objects.create()
        List.objects.create()

        response = self.client.post(('/lists/' +
                                     str(correct_list.id) + '/'),
                                    data={'text':
                                          'A new item for an existing list'})

        self.assertRedirects(response, '/lists/' + str(correct_list.id) + '/')

    def post_invalid_input(self):
        list_ = List.objects.create()
        return self.client.post(
            '/lists/' + str(list_.id) + '/', data={'text': ''})

    def test_for_invalid_input_nothing_saved_to_db(self):
        self.post_invalid_input()
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_list_template(self):
        response = self.post_invalid_input()
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(response.status_code, 200)

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.post_invalid_input()
        self.assertIsInstance(response.context['form'], ExistingListItemForm)

    def test_for_invalid_input_shows_errors_on_page(self):
        """
        CHECK THAT FORM IS RENDERED AND ERRORS ARE DISPLAYED
        """
        response = self.post_invalid_input()
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
        list_ = List.objects.create()
        Item.objects.create(list=list_, text="hey john")
        response = self.client.post(
            '/lists/' + str(list_.id) + '/',
            data={"text": "hey john"}
        )
        expected_error = escape(DUPLICATE_ITEM_ERROR)
        self.assertContains(response, expected_error)
        self.assertTemplateUsed(response, "list.html")
        self.assertEqual(Item.objects.count(), 1)


class NewListTest(TestCase):

    def test_invalid_list_items_arent_saved(self):
        self.client.post('/lists/new', data={'text': ''})
        self.assertEqual(List.objects.count(), 0)
        self.assertEqual(Item.objects.count(), 0)

    def test_for_invalid_input_renders_home_template(self):
        response = self.client.post('/lists/new', data={"text": ""})
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home.html")

    def test_validation_errors_are_shown_on_home_page(self):
        response = self.client.post('/lists/new', data={"text": ""})
        self.assertContains(response, escape(EMPTY_ITEM_ERROR))

    def test_for_invalid_input_passes_form_to_template(self):
        response = self.client.post('/lists/new', data={"text": ""})
        self.assertIsInstance(response.context['form'], ItemForm)

    def test_can_save_a_POST_request(self):
        self.client.post('/lists/new', data={"text": "A new list item"})
        self.assertEqual(Item.objects.count(), 1)
        new_item = Item.objects.first()
        self.assertEqual(new_item.text, "A new list item")

    def test_redirects_after_POST(self):
        response = self.client.post(
            '/lists/new', data={"text": "A new list item"})
        new_list = List.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/lists/' + str(new_list.id) + '/')
