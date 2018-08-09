from django.test import TestCase
from django.urls import resolve
from django.http import HttpRequest

from .views import home_page
from .models import Item

class HomePageTest(TestCase):    
    def test_uses_home_template(self):        
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')
    

    def test_can_save_a_POST_request(self):
        response = self.client.post('/', data={"item_text": "A new list Item"})
        self.assertEqual(Item.objects.count(), 1)
        saved_item = Item.objects.first()
        self.assertEqual(saved_item.text, "A new list Item")

  
    def test_redirects_after_POST(self):
        response = self.client.post('/', data={"item_text": "A new list Item"})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')


    def test_only_save_item_when_necessary(self):
    	response = self.client.get('/')
    	self.assertEqual(Item.objects.count(), 0)


class ItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertIn("The first (ever) list item", first_saved_item.text)
        self.assertIn("Item the second", second_saved_item.text)


class ListViewTest(TestCase):
    def test_displays_all_list_items(self):
    	Item.objects.create(text="item 1")
    	Item.objects.create(text="item 2")
    	response = self.client.get('/lists/the-only-list-in-the-world/')
    	self.assertContains(response, "item 1")
    	self.assertContains(response, "item 2")

    def test_uses_list_template(self):
    	response = self.client.get('/lists/the-only-list-in-the-world/')
    	self.assertTemplateUsed(response, "list.html")
