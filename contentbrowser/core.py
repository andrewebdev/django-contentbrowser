from django.conf import settings
from django.contrib.contenttypes.models import ContentType

from appregister import Registry


class CBRegistry(Registry):
    base = 'contentbrowser.core.ContentBrowser'
    discovermodule = 'cbitems'

cbregistry = CBRegistry()


class ContentBrowser(object):
    title = None
    content_type = None

    def get_items(self, request):
        return None
