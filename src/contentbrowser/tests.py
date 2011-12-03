from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings

from core import ContentBrowser
from views import BrowserItemsView
from templatetags.contentbrowser_tags import show_contentbrowser


## Create some test models that we can use
class DemoModel(models.Model):
	name = models.CharField(max_length=100)
	description = models.TextField()
	is_visible = models.BooleanField(default=False)

class SecondDemoModel(models.Model):
	name = models.CharField(max_length=20)
	is_visible = models.BooleanField(default=True)

CONTENT_BROWSER_TYPES = ('contentbrowser.demomodel', 'contentbrowser.seconddemomodel')


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

		## Make sure the ContentBrowser is completely empty
		self.cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)

	def test_content_browser_models_registered_on_init(self):
		cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)
		self.assertEqual(
			('contentbrowser.demomodel', 'contentbrowser.seconddemomodel'),
			cb._registered_types)

	def test_get_categories(self):
		expected_list = [
			{
				'contenttype': 'contentbrowser.demomodel',
				'verbose_name': 'Demo Model',
				'verbose_name_plural': 'Demo Models'
			},
			{
				'contenttype': 'contentbrowser.seconddemomodel',
				'verbose_name': 'Second Demo Model',
				'verbose_name_plural': 'Second Demo Models'
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


class ContentBrowserInclusionTagTestCase(TestCase):

	def setUp(self):
		DemoModel.objects.create(
			name='Demo 1', description='Demo 1 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=False)

		## Make sure the ContentBrowser is completely empty
		self.cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)


class BrowserItemsViewTestCase(TestCase):

	urls = 'contentbrowser.urls'

	def setUp(self):
		settings.CONTENT_BROWSER_RESTRICTED_TO = None

		DemoModel.objects.create(
			name='Demo 1', description='Demo 1 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=False)

		# Create a test user instance
		self.user = User.objects.create(username='user1', password='secret')
		self.user.save()

		## Make sure the ContentBrowser is completely empty
		self.cb = ContentBrowser(custom_types=CONTENT_BROWSER_TYPES)

	def test_browser_items_view_exists(self):
		items_view = BrowserItemsView()

	def test_browser_items_view_status(self):
		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(200, response.status_code)

	def test_browser_items_view_context(self):
		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(True, response.context_data['empty_items'])

	def test_browser_items_with_ctypes(self):
		rf = RequestFactory()
		request = rf.get('/?ctype=contentbrowser.demomodel')
		request.user = self.user
		response = BrowserItemsView.as_view()(request)

		expected_items = [1, 2, 3]

		self.assertEqual(
			expected_items,
			list(response.context_data['contentbrowser_demomodel_items']\
				.values_list('id', flat=True))
		)

	def test_only_permitted_groups_have_access(self):
		settings.CONTENT_BROWSER_RESTRICTED_TO = ('group1', 'group2')

		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(403, response.status_code)

	def test_permitted_groups_have_access(self):
		settings.CONTENT_BROWSER_RESTRICTED_TO = ('group1', 'group2')
		group = Group.objects.create(name='group1')
		self.user.groups.add(group)

		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(200, response.status_code)


class BrowserItemsURLTestCase(TestCase):

	urls = 'contentbrowser.urls'

	def test_reverse_lookup(self):
		self.assertEqual('/browse/items/', reverse('contentbrowser_browse_items'))
