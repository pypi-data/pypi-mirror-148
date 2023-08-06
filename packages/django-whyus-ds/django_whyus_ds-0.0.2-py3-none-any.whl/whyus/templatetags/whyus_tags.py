from django.template import Library, loader

import logging
logger = logging.getLogger(__name__)
formatter = logging.Formatter('%(levelname)s: [%(name)s] %(message)s')
ch = logging.StreamHandler()
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.setLevel(logging.ERROR)


register = Library()

# https://localcoder.org/django-inclusion-tag-with-configurable-template


@register.simple_tag(takes_context=True)
def make_whyus(context):
    logger.info(context)
    t = loader.get_template(f"whyus/{context['theme']}.html")
    c = {
        'theme': context['theme'],
        'whyus': context['whyus']
    }
    return t.render(c)
