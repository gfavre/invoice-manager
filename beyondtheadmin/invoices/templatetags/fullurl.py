import math

from django import template
from django.utils.safestring import mark_safe


register = template.Library()


@register.simple_tag(takes_context=True)
def buildfullurl(context, url):
    """Converts relative URL to absolute.
    For example:
        {% buildfullurl article.get_absolute_url %}
    or:
        {% buildfullurl "/custom-url/" %}
    """
    return context.request.build_absolute_uri(url)


@register.filter(
    is_safe=True,
)
def add_domain(value):
    try:
        number = float(value)
        frac, integer = math.modf(number)
        if frac:
            return mark_safe(f'CHF <span class="value">{number:1,.2f}</span>'.replace(",", "'"))
        return mark_safe(f'CHF <span class="value">{number:1,.0f}.-</span>'.replace(",", "'"))
    except (ValueError, TypeError):
        return value
