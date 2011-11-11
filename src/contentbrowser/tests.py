from django.test import TestCase
from django.db import models
from django.conf import settings

from core import ContentBrowser


## Create a test model that we can use
class DemoModel(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	is_visible = models.BooleanField(default=False)


CONTENT_BROWSER_TYPES = ('contentbrowser.demomodel',)


## Commence tests :)
class DemoModelTestCase(TestCase):

	def test_demo_model(self):
		demo = DemoModel(name='Demo 1', description='Demo 1 Description',
			is_visible=True)


class ContentBrowserTestCase(TestCase):

	def setUp(self):
		DemoModel.objects.create(
			name='Demo 1', description='Demo 1 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=False)

		self.cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)

	def test_content_browser_models_registered_on_init(self):
		cb = ContentBrowser()
		self.assertEqual(None, cb._registered_types)

		cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)
		self.assertEqual(('contentbrowser.demomodel',), cb._registered_types)

	def test_get_categories(self):
		expected_list = [
			{
				'contenttype': 'contentbrowser.demomodel',
				'verbose_name': 'Demo Model',
				'verbose_name_plural': 'Demo Models'
			}
		]
		self.assertEqual(expected_list, self.cb.get_types())

	def test_get_model_class(self):
		self.assertEqual(DemoModel, self.cb.get_model_for('contentbrowser.demomodel'))

	def test_get_items_for(self):
		item_list = list(
			self.cb.get_items_for('contentbrowser.demomodel')\
			.values_list('id', flat=True))

		self.assertEqual([1, 2, 3], item_list)

	def test_get_items_for_with_custom_queryset(self):
		self.cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)
		qs = DemoModel.objects.filter(is_visible=True)
		self.cb.set_queryset_for('contentbrowser.demomodel', qs)

		item_list = list(
			self.cb.get_items_for('contentbrowser.demomodel')\
			.values_list('id', flat=True))
		
		self.assertEqual([1, 2], item_list)



