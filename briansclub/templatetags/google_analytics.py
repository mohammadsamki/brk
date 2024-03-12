from django import template
from briansclub.models import SiteConfiguration
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def google_analytics():
    try:
        site_config = SiteConfiguration.objects.first()
        ga_id = site_config.google_analytics_id
    except SiteConfiguration.DoesNotExist:
        ga_id = ''
    return mark_safe(f"""
        <script async src="https://www.googletagmanager.com/gtag/js?id={ga_id}"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){{dataLayer.push(arguments);}}
            gtag('js', new Date());
            gtag('config', '{ga_id}');
        </script>
    """)