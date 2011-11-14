from django.conf import settings


def actions(request):
    CB_ACTIONS_PATH = getattr(
        settings, 'CONTENTBROWSER_ACTIONS_PATH', 'js/cb_actions.js')
    return {
        'CB_ACTIONS_PATH': CB_ACTIONS_PATH,
    }