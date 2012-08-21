from django import forms
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.conf import settings

from contentbrowser.core import ContentBrowser, cbregistry


STATIC_URL = getattr(settings, 'STATIC_URL')
CONTENT_BROWSER_ACTIONS_PATH = (settings, 'CONTENT_BROWSER_ACTIONS_PATH',
    '%sjs/cb_actions.js' % STATIC_URL)


class CBWidgetMixin(object):
    """ Use this mixin to add the ContentBrowser existing widgets. """

    def _media(self):
        """
        Since this mixin doesn't inherrit from an existing widget, we
        recreate the media property, so that we dont overwrite
        the media for other widgets
        """
        return forms.Media(
            css = {
                'all': (
                    '%scontentbrowser/css/cb.css' % STATIC_URL,
                ),
            },
            js = (
                '%scontentbrowser/js/contentbrowser.js' % STATIC_URL,
                CONTENT_BROWSER_ACTIONS_PATH,
            )
        )
    media = property(_media)

    def render(self, name, value, attrs=None, **kwargs):
        rendered = super(CBWidgetMixin, self).render(name, value, attrs)

        contenttypes = []
        for category in cbregistry.all():
            contenttypes.append({
                'contenttype': category.content_type,
                'name': category.title,
            })

        context = {
            'contenttypes': contenttypes,
            'name': name,
            'STATIC_URL': STATIC_URL,
        }

        return rendered + mark_safe(render_to_string(
            'widgets/cb_widget.html', context))
