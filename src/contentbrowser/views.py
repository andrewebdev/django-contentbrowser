from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
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
        page = self.request.GET.get('page', 1)

        cb = ContentBrowser()

        if ctype:
            CONTENT_BROWSER_ITEM_COUNT = getattr(
                settings, 'CONTENT_BROWSER_ITEM_COUNT', 8)

            item_list = cb.get_items_for(ctype, refresh_cache=True)
            paginator = Paginator(item_list, CONTENT_BROWSER_ITEM_COUNT)

            try:
                page = paginator.page(page)

            except PageNotAnInteger:
                page = paginator.page(1)
            
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            c['ctype'] = ctype
            c['page'] = page

        else:
            c['empty_items'] = True

        return c
