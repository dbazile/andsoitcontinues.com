import glob
import logging
import os
import re

import yaml
from markdown import markdown

DATE_FORMAT_INPUT = '%Y-%m-%d'
DEFAULT_TYPE = 'text'
TYPE_IMAGE = 'image'
TYPE_QUOTE = 'quote'
TYPE_LINK = 'link'
TYPE_TEXT = 'text'

PATTERN_MARKDOWN = re.compile("""^---\n(?P<meta>.*)\n---\n\n?(?P<body>.*)$""",
                              re.MULTILINE | re.DOTALL)

log = logging.getLogger(__name__)


def clean(output_dir):
    filepaths = glob.glob(os.path.join(output_dir, 'writing/*.html'))
    filepaths.append(os.path.join(output_dir, 'index.html'))
    for filepath in filepaths:
        log.info('clean %s', os.path.relpath(filepath))
        os.unlink(filepath)


def render(env, markdown_dir, output_dir):
    posts = []
    failures = []

    for filepath in glob.glob(os.path.join(markdown_dir, '*.md')):
        filepath = os.path.relpath(filepath)
        try:
            post = _deserialize_post(filepath)
            _render_post(env, post, output_dir)
            posts.append(post)
        except ValidationError as err:
            failures.append(filepath)
            log.error('Failed on %s: %s', filepath, err)
        except Exception as err:
            log.fatal('Could not process `%s`\n\t%s: %s',
                      filepath, err.__class__.__name__, err)
            raise

    posts = sorted(posts, reverse=True, key=lambda p: p['date'])
    _render_index(env, posts, output_dir)

    # Report card
    if failures:
        log.warning('*** %s failures: %s', len(failures), ', '.join(failures))


###############################################################################

#
# Internals
#

def _deserialize_post(filepath):
    log.debug('_deserialize_post:READ %s', filepath)
    with open(filepath) as fp:
        matches = PATTERN_MARKDOWN.search(fp.read())
    if not matches:
        raise ValueError('missing metadata')

    raw_meta, raw_body = matches.groups()

    post = {
        'id': _generate_id(filepath),
        'type': DEFAULT_TYPE,
        'body': markdown(raw_body, [
            'markdown.extensions.smarty',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.toc',
        ]),
    }

    for key, value in yaml.load(raw_meta).items():
        key = key.lower()
        if key not in ('abstract', 'date', 'subject', 'tags', 'type', 'url'):
            return

        if key == 'abstract':
            value = markdown(value, extensions=['markdown.extensions.smarty'])

        post[key] = value
    _validate(post)

    # Special Case: Quotes and images need abstract to mirror body
    if post['type'] in ('quote', 'image'):
        post['abstract'] = post['body']

    return post


def _generate_id(filepath):
    basename, _ = os.path.splitext(os.path.basename(filepath))
    return re.sub(r'\W+', '_', basename)


def _render_post(env, post: dict, output_dir):
    template = env.get_template('_blog.post.jinja2')

    context = post.copy()

    # Type-specific Logic
    if context['type'] == TYPE_IMAGE:
        context['body'] = '<img src="{0}"/>'.format(context['url'])
    elif context['type'] == TYPE_QUOTE:
        context['abstract'] = ''
    elif context['type'] == TYPE_LINK:
        context['body'] = '<a href="{0}">{0}</a>'.format(context['url'])

    # Write file
    filepath = os.path.relpath(os.path.join(output_dir, 'writing/{0}.html'.format(post['id'])))
    log.debug('_render_post:Before write `%s`', filepath)
    with open(filepath, 'w') as fp:
        fp.write(template.render(**context))
    log.info('OK %s', filepath)


def _render_index(env, posts, output_dir):
    template = env.get_template('_blog.index.jinja2')

    contexts = []
    for post in posts:
        context = post.copy()
        if context['type'] in (TYPE_TEXT, TYPE_QUOTE):
            context['url'] = 'writing/{0}.html'.format(post['id'])
        contexts.append(context)

    filepath = os.path.relpath(os.path.join(output_dir, 'index.html'))
    with open(filepath, 'w') as fp:
        log.debug('_render_index:Before write `%s`', filepath)
        fp.write(template.render(posts=contexts))
    log.info('OK %s', filepath)


def _validate(post):
    # Required fields
    for key in ('id', 'type', 'tags', 'subject'):
        if key not in post:
            raise ValidationError('missing `{}`'.format(key), post)

    # Images and Links must point to something
    if post.get('type') in ('image', 'link'):
        if 'url' not in post:
            raise ValidationError('missing `{}`'.format('url'), post)


#
# Errors
#

class ValidationError(Exception):
    def __init__(self, message, post):
        self.message = message
        self.post = post

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.message)
