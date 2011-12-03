from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django import http
from django.conf import settings

from core import ContentBrowser


class BrowserItemsView(TemplateView):
    template_name = 'contentbrowser/browser_items.html'

    def get(self, *args, **kwargs):
        user_groups = self.request.user.groups.values_list('name', flat=True)
        CONTENT_BROWSER_RESTRICTED_TO = getattr(
            settings, 'CONTENT_BROWSER_RESTRICTED_TO', None)

        if not CONTENT_BROWSER_RESTRICTED_TO:
            return super(BrowserItemsView, self).get(*args, **kwargs)

        for group in user_groups:
            if group in CONTENT_BROWSER_RESTRICTED_TO:
                return super(BrowserItemsView, self).get(*args, **kwargs)

        return http.HttpResponseForbidden()

    def get_context_data(self, **kwargs):
        c = super(BrowserItemsView, self).get_context_data(**kwargs)
        ctype = self.request.GET.get('ctype', None)
        cb = ContentBrowser()
        if ctype:
            c['%s_items' % ctype.replace('.', '_')] = cb.get_items_for(
                ctype, refresh_cache=True)
        else:
            c['empty_items'] = True
        return c
