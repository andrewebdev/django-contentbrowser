from django.views.generic import TemplateView

from core import ContentBrowser


class BrowserItemsView(TemplateView):
	template_name = 'contentbrowser/browser_items.html'

	def get_context_data(self, **kwargs):
		c = super(BrowserItemsView, self).get_context_data(**kwargs)
		ctypes = self.request.GET.get('ctypes', None)
		cb = ContentBrowser()
		if ctypes:
			for ct in ctypes.split(','):
				c['%s_items' % ct.replace('.', '_')] = cb.get_items_for(ctypes)
		else:
			c['empty_items'] = True
		return c
