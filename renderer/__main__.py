import argparse
import datetime
import logging
import os

from jinja2 import Environment, FileSystemLoader

from renderer import blog, partials, portfolio


WEB_ROOT     = 'public'
MARKDOWN_DIR = 'data/markdown'
XML_DIR      = 'data/xml'
TEMPLATE_DIR = 'renderer/templates'


# Collect script params
parser = argparse.ArgumentParser()
parser.add_argument('--debug', action='store_true')
parser.add_argument('--clean', action='store_true')
parser.add_argument('--clean-only', action='store_true')
parser.add_argument('--watch', action='store_true')
options = parser.parse_args()


# Enter workspace
os.chdir(os.path.dirname(os.path.dirname(__file__)))


# Configure logging
logging.basicConfig(
    datefmt='%H:%M:%S',
    format='%(asctime)s [%(name)s:%(funcName)s] %(levelname)-7s - %(message)s' if options.debug else '[%(name)-18s] %(levelname)s : %(message)s',
    level='DEBUG' if options.debug else 'INFO',
)


# Prepare Jinja2
env = Environment(
    loader=FileSystemLoader(TEMPLATE_DIR),
    lstrip_blocks=True,
    trim_blocks=True,
)
env.filters['format_datetime'] = datetime.datetime.strftime


# Execute
if options.clean or options.clean_only:
    blog.clean(WEB_ROOT)
    portfolio.clean(WEB_ROOT)
    partials.clean(WEB_ROOT)

    if options.clean_only:
        exit()

if options.watch:
    blog.watch(env, MARKDOWN_DIR, WEB_ROOT)
else:
    blog.render(env, MARKDOWN_DIR, WEB_ROOT)
    portfolio.render(env, XML_DIR, WEB_ROOT)
    partials.render(env, WEB_ROOT)
