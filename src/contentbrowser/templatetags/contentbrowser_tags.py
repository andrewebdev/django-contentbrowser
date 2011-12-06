from django import template

from contentbrowser.core import ContentBrowser, cbregistry

register = template.Library()


@register.inclusion_tag('contentbrowser/show_contentbrowser.html')
def show_contentbrowser():
    
    contenttypes = []

    for category in cbregistry.all():
        contenttypes.append({
            'contenttype': category.content_type,
            'name': category.title,
        })

    return {'contenttypes': contenttypes}