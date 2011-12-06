from django.test import TestCase
from django.test.client import RequestFactory, Client
from django.db import models
from django.contrib.auth.models import User, Group
from django.core.urlresolvers import reverse
from django.conf import settings

from core import ContentBrowser, cbregistry
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


## Commence tests :)
class DemoModelTestCase(TestCase):

	def test_demo_model(self):
		demo = DemoModel(name='Demo 1', description='Demo 1 Description',
			is_visible=True)


@cbregistry.register
class DemoModelItems(ContentBrowser):
    content_type = 'contentbrowser.demomodel'
    title = 'Demo Model'

    def get_items(self, request):
        return DemoModel.objects.all()


class ContentBrowserTestCase(TestCase):

	def test_contentbrowser_class(self):
		ContentBrowser

	def test_defaults(self):
		self.assertEqual(None, ContentBrowser.title)
		self.assertEqual(None, ContentBrowser.content_type)

	def test_instance_get_items(self):
		rf = RequestFactory()
		request = rf.get('/')

		cb = ContentBrowser()	
		self.assertEqual(None, cb.get_items(request))


class ContentBrowserRegistry(TestCase):

	def setUp(self):
		DemoModel.objects.create(
			name='Demo 1', description='Demo 1 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=True)
		DemoModel.objects.create(
			name='Demo 2', description='Demo 2 Description', is_visible=False)

		self.rf = RequestFactory()

	def test_browser_in_registry(self):
		classes = cbregistry.all()
		self.assertIn(DemoModelItems, classes)

	def test_browser_title(self):
		for cb in cbregistry:
			if cb.content_type == 'contentbrowser.demomodel':
				browser = cb()
				break

		self.assertEqual('Demo Model', browser.title)

	def test_browser_get_items(self):
		request = self.rf.get('/')

		for cat in cbregistry:
			if cat.content_type == 'contentbrowser.demomodel':
				category = cat()
				break

		expected_items = [1, 2, 3]
		item_list = category.get_items(request).values_list('id', flat=True)

		self.assertEqual(expected_items, list(item_list))


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

	def test_browser_items_view_exists(self):
		items_view = BrowserItemsView()

	def test_browser_items_view_status(self):
		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(200, response.status_code)

	def test_browser_items_empty_context(self):
		rf = RequestFactory()
		request = rf.get('/')
		request.user = self.user

		response = BrowserItemsView.as_view()(request)
		self.assertEqual(True, response.context_data['empty_items'])

	def test_browser_items_context(self):
		rf = RequestFactory()
		request = rf.get('/?ctype=contentbrowser.demomodel')
		request.user = self.user
		response = BrowserItemsView.as_view()(request)

		self.assertIn('page', response.context_data)
		self.assertIn('ctype', response.context_data)

	def test_browser_items_with_ctypes(self):
		rf = RequestFactory()
		request = rf.get('/?ctype=contentbrowser.demomodel')
		request.user = self.user
		response = BrowserItemsView.as_view()(request)

		expected_items = [1, 2, 3]
		items = response.context_data['page'].object_list\
			.values_list('id', flat=True)

		self.assertEqual('contentbrowser.demomodel',
			response.context_data['ctype'])

		self.assertEqual(expected_items, list(items))

	def test_browser_items_paginated(self):
		rf = RequestFactory()
		request = rf.get('/?ctype=contentbrowser.demomodel')
		request.user = self.user
		response = BrowserItemsView.as_view()(request)

		self.assertEqual('Page',
			response.context_data['page'].__class__.__name__)

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


