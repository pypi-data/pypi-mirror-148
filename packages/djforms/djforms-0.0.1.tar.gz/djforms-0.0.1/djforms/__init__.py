
def setup_settings(settings, is_prod, **kwargs):

    settings['INSTALLED_APPS'] += [
        app for app in [
            'widget_tweaks',
            'crispy_forms'
        ] if app not in settings['INSTALLED_APPS']
    ]
