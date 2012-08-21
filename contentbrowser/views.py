from django.views.generic import TemplateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django import http
from django.conf import settings

from core import ContentBrowser, cbregistry


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
        cb = self.request.GET.get('cb')
        page = self.request.GET.get('page', 1)

        category = None
        for cat in cbregistry:
            if cat.content_type == ctype:
                category = cat()
                break

        if ctype and category:
            CONTENT_BROWSER_ITEM_COUNT = getattr(
                settings, 'CONTENT_BROWSER_ITEM_COUNT', 8)

            item_list = category.get_items(self.request)
            paginator = Paginator(item_list, CONTENT_BROWSER_ITEM_COUNT)

            try:
                page = paginator.page(page)

            except PageNotAnInteger:
                page = paginator.page(1)
            
            except EmptyPage:
                page = paginator.page(paginator.num_pages)

            c['ctype'] = ctype
            c['page'] = page
            c['cb'] = cb

        else:
            c['empty_items'] = True

        return c
