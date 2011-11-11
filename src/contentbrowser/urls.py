from django.conf.urls.defaults import *

from views import BrowserItemsView


urlpatterns = patterns('',
	url(r'^browse/items/$', BrowserItemsView.as_view(),
		name="contentbrowser_browser_items"),
)