from django import template

from contentbrowser.core import ContentBrowser

register = template.Library()


@register.inclusion_tag('contentbrowser/show_contentbrowser.html')
def show_contentbrowser():
	cb = ContentBrowser()
	contenttypes = []
	for ctype in cb.get_types():
		contenttypes.append({
			'contenttype': ctype['contenttype'],
			'name': ctype['verbose_name_plural']
		})
	return {'contenttypes': contenttypes}