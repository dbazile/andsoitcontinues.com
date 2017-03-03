import datetime
import logging
import os
import sys

from jinja2 import Environment, FileSystemLoader

from renderer import blog, partials, portfolio

ROOT         = os.path.dirname(os.path.dirname(__file__))
WEB_ROOT     = os.path.join(ROOT, 'web')
MARKDOWN_DIR = os.path.join(ROOT, 'data/markdown')
XML_DIR      = os.path.join(ROOT, 'data/xml')
TEMPLATE_DIR = os.path.join(ROOT, 'renderer/templates')

logging.basicConfig(
    level=logging.DEBUG if '-d' in sys.argv else logging.INFO,
)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    lstrip_blocks=True,
    trim_blocks=True,
)

env.filters['format_datetime'] = datetime.datetime.strftime
if 'clean' in sys.argv:
    blog.clean(WEB_ROOT)
    portfolio.clean(WEB_ROOT)
    partials.clean(WEB_ROOT)
else:
    blog.render(env, MARKDOWN_DIR, WEB_ROOT)
    portfolio.render(env, XML_DIR, WEB_ROOT)
    partials.render(env, WEB_ROOT)
