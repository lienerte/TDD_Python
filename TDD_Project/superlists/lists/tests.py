from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from views import home_page
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.

class InitialTest(TestCase):

    def test_root_url_resolves_to_home_page(self):
        found = resolve('/')
        self.assertEqual(found.func, home_page)

    def test_home_page_returns_correct(self):
        request = HttpRequest()
        response = home_page(request)
        expected_html = render_to_string('home.html', request = request)
        self.assertEqual(response.content.decode(), expected_html)

    def test_home_page_can_save_a_POST_request(self):
    		#Setup
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'
        	#Exercise
        response = home_page(request)

        #self.assertEqual(Item.objects.count(), 1)
        #new_item = Item.objects.first()
        	#Assert

        self.assertIn('A new list item', response.content.decode())
        expected_html = render_to_string (
        	'home.html',
        	{'new_item_list': request.POST.get('item_text','')
        }, request = request)
        self.assertEqual(response.content.decode(), expected_html)

class ItemModelTest(TestCase):

	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = "The first list item"
		first_item.save()

		second_item = Item()
		second_item.text = "The second item"
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, "The first list item")
		self.assertEqual(second_saved_item.text, "The second item")

