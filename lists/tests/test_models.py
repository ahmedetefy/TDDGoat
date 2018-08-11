from django.test import TestCase
# from django.urls import resolve
# from django.http import HttpRequest

# from .views import home_page
from ..models import Item, List


class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = "The first (ever) list item"
        first_item.list = list_
        first_item.save()

        second_item = Item()
        second_item.text = "Item the second"
        second_item.list = list_
        second_item.save()

        saved_list = List.objects.first()
        self.assertEqual(list_, saved_list)

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertIn("The first (ever) list item", first_saved_item.text)
        self.assertEqual(first_saved_item.list, list_)
        self.assertIn("Item the second", second_saved_item.text)
        self.assertEqual(second_saved_item.list, list_)

