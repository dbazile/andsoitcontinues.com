import sys
import logging
from datetime import datetime
from os.path import dirname, join
from jinja2 import Environment, FileSystemLoader
from renderer import blog, partials, portfolio

ROOT = dirname(dirname(__file__))
MARKDOWN_DIR = join(ROOT, 'data/markdown')
XML_DIR = join(ROOT, 'data/xml')
TEMPLATE_DIR = join(ROOT, 'renderer/templates')

logging.basicConfig(
    level=logging.DEBUG if '-d' in sys.argv else logging.INFO,
)

env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    lstrip_blocks=True,
    trim_blocks=True,
)

env.filters['format_datetime'] = datetime.strftime

blog.render(env, MARKDOWN_DIR, ROOT)
portfolio.render(env, XML_DIR, ROOT)
partials.render(env, ROOT)
