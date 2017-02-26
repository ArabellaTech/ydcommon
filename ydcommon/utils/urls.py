try:
    from django.urls import reverse
except ImportError:
    # Django < 2.0
    from django.core.urlresolvers import reverse
