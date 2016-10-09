from datetime import datetime
from glob import glob
from logging import getLogger
from os import path
import re

import markdown

DATE_FORMAT_INPUT = '%Y-%m-%d'
DEFAULT_TYPE = 'text'
TYPE_IMAGE = 'image'
TYPE_QUOTE = 'quote'
TYPE_LINK = 'link'
TYPE_TEXT = 'text'

log = getLogger(__name__)


def render(env, markdown_dir, output_dir):
    posts = []
    failures = []

    for filepath in glob(path.join(markdown_dir, '*.md')):
        filepath = path.relpath(filepath)
        try:
            post = _deserialize_post(filepath)
            _render_post(env, post, output_dir)
            posts.append(post)
        except ValidationError as err:
            failures.append(filepath)
            log.error('Failed on {}: {}'.format(filepath, err))
        except Exception as err:
            log.fatal('Could not process `{}`\n\t{}: {}'.format(filepath, err.__class__.__name__, err))
            raise err

    posts = sorted(posts, reverse=True, key=lambda p: p['date'])
    _render_index(env, posts, output_dir)

    # Report card
    if failures:
        log.warn('*** {} failures: {}'.format(len(failures), ', '.join(failures)))


################################################################################

#
# Internals
#

def _deserialize_post(filepath):
    parser = markdown.Markdown(extensions=[
        'markdown.extensions.meta',
        'markdown.extensions.smarty',
        'markdown.extensions.fenced_code'
    ])

    log.debug('_deserialize_post:READ {}'.format(filepath))
    with open(filepath) as fp:
        serialized = fp.read()

    post = {
        'id': _generate_id(filepath),
        'type': DEFAULT_TYPE,
        'body': parser.convert(serialized),
    }
    for key, value in parser.Meta.items():
        if key in ('abstract', 'date', 'subject', 'tags', 'type', 'url'):
            value = value.pop()

            # Normalize meta properties
            if key == 'tags':
                value = [s.strip() for s in value.split(',')]
            elif key == 'abstract':
                value = markdown.markdown(value, extensions=['markdown.extensions.smarty'])
            elif key == 'date':
                value = datetime.strptime(value, DATE_FORMAT_INPUT)

            post[key] = value
    _validate(post)

    # Special Case: Quotes and images need abstract to mirror body
    if post['type'] in ('quote', 'image'):
        post['abstract'] = post['body']

    return post


def _generate_id(filepath):
    basename, _ = path.splitext(path.basename(filepath))
    return re.sub(r'\W+', '_', basename)


def _render_post(env, post: dict, output_dir):
    template = env.get_template('_blog.post.html')

    context = post.copy()

    # Type-specific Logic
    if context['type'] == TYPE_IMAGE:
        context['body'] = '<img src="{0}"/>'.format(context['url'])
    elif context['type'] == TYPE_QUOTE:
        context['abstract'] = ''
    elif context['type'] == TYPE_LINK:
        context['body'] = '<a href="{0}">{0}</a>'.format(context['url'])

    # Write file
    filepath = path.relpath(path.join(output_dir, 'writing/{0}.html'.format(post['id'])))
    log.debug('_render_post:Before write `{}`'.format(filepath))
    with open(filepath, 'w') as fp:
        fp.write(template.render(**context))
    log.info('OK {0}'.format(filepath))


def _render_index(env, posts, output_dir):
    template = env.get_template('_blog.index.html')

    contexts = []
    for post in posts:
        context = post.copy()
        if context['type'] in (TYPE_TEXT, TYPE_QUOTE):
            context['url'] = 'writing/{0}.html'.format(post['id'])
        contexts.append(context)

    filepath = path.relpath(path.join(output_dir, 'index.html'))
    with open(filepath, 'w') as fp:
        log.debug('_render_index:Before write `{}`'.format(filepath))
        fp.write(template.render(posts=contexts))
    log.info('OK {}'.format(filepath))


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
