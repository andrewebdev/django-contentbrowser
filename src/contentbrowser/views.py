from django.views.generic import TemplateView

from core import ContentBrowser

class BrowserItemsView(TemplateView):
	template_name = 'contentbrowser/browser_items.html'

	def get_context_data(self, **kwargs):
		c = super(BrowserItemsView, self).get_context_data(**kwargs)
		ctype = self.request.GET.get('ctype', None)
		cb = ContentBrowser()
		if ctype:
			c['%s_items' % ctype.replace('.', '_')] = cb.get_items_for(ctype)
		else:
			c['empty_items'] = True
		return c
