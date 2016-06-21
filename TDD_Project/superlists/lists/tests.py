from django.test import TestCase
from django.core.urlresolvers import resolve
from django.http import HttpRequest
from views import home_page
from django.template.loader import render_to_string

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
        	{'new_item_list': request.POST.get('item_text',''),
        })
        self.assertEqual(response.content.decode(), expected_html)
