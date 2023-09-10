from django.test import TestCase
import unittest
from .models import Event, Review, Category, Bookmark, Organizer, Media, Ticket


class CategoryTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        Category.objects.create(name='Example')

    def test_your_model_method(self):
        obj = Category.objects.get(name='Example')
        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), 'Example')


class EventTestCase(TestCase):
    def setUp(self):
        # Set up any necessary data for the tests
        Event.objects.create(title='Make sure to import the model class in your test file so that you can create an instance of it and call its methods for testing',
                             venue='venue',description='description',creator=4,date='2023-06-09 17:16:38.397174+00',category='entertainment',ticket_price='250')

    def test_your_model_method(self):
        obj = Event.objects.get(title='Make sure to import the model class in your test file so that you can create an instance of it and call its methods for testing')
        # Test the behavior of your model method
        self.assertEqual(obj.__str__(), 'Done')