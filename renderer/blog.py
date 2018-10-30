import glob
import logging
import os
import re

import yaml
from markdown import markdown


DEFAULT_TYPE = 'text'
TYPE_IMAGE = 'image'
TYPE_QUOTE = 'quote'
TYPE_LINK = 'link'
TYPE_TEXT = 'text'

FILEPATH        = 'writing/{date:%Y}/{id}.html'
LEGACY_FILEPATH = 'writing/{id}.html'

PATTERN_MARKDOWN = re.compile('''^---\n(?P<meta>.*)\n---\n\n?(?P<body>.*)$''',
                              re.MULTILINE | re.DOTALL)

LOG = logging.getLogger(__name__)


def clean(output_dir):
    filepaths = glob.glob(os.path.join(output_dir, 'writing/*.html'))
    filepaths.extend(glob.glob(os.path.join(output_dir, 'index.html')))
    filepaths.extend(glob.glob(os.path.join(output_dir, 'writing/2???/*.html')))
    for filepath in filepaths:
        LOG.info('clean %s', filepath)
        os.unlink(filepath)


def render(env, markdown_dir, output_dir):
    posts = []
    failures = []

    for filepath in glob.glob(os.path.join(markdown_dir, '*.md')):
        try:
            post = _deserialize_post(filepath)
            _render_post(env, post, output_dir)
            posts.append(post)
        except ValidationError as err:
            failures.append(filepath)
            LOG.error('Failed on %s: %s', filepath, err)
        except Exception as err:
            LOG.fatal('Could not process `%s`\n\t%s: %s',
                      filepath, err.__class__.__name__, err)
            raise

    posts = sorted(posts, reverse=True, key=lambda p: p['date'])
    _render_index(env, posts, output_dir)

    # Report card
    if failures:
        LOG.warning('*** %s failures: %s', len(failures), ', '.join(failures))


###############################################################################

#
# Internals
#

def _deserialize_post(filepath):
    LOG.debug('READ %s', filepath)

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
    template = env.get_template('blogpost.jinja2')

    context = post.copy()

    # Type-specific Logic
    if context['type'] == TYPE_IMAGE:
        context['body'] = '<img src="{0}"/>'.format(context['url'])
    elif context['type'] == TYPE_QUOTE:
        context['abstract'] = ''
    elif context['type'] == TYPE_LINK:
        context['body'] = '<a href="{0}">{0}</a>'.format(context['url'])

    filepath = os.path.join(output_dir, FILEPATH.format(**post))

    # Ensure parent dir
    parent_dir = os.path.dirname(filepath)
    if not os.path.exists(parent_dir):
        LOG.debug('Creating parent dir `%s`', parent_dir)
        os.makedirs(parent_dir)

    LOG.debug('Before write `%s`', filepath)
    with open(filepath, 'w') as fp:
        fp.write(template.render(**context))

    # HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK
    # Copy output to unqualified path to avoid breaking old links
    legacy_filepath = os.path.join(output_dir, LEGACY_FILEPATH.format(**post))
    LOG.debug('Copy to unqualified location `%s`', legacy_filepath)
    with open(legacy_filepath, 'w') as fp:
        fp.write(template.render(**context).replace(
            '<head>',
            '<head>\n\n  <meta http-equiv="refresh" content="0; url=/{}" />\n'.format(FILEPATH.format(**post)),
        ))
    # HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK HACK

    LOG.info('wrote %s', filepath)


def _render_index(env, posts, output_dir):
    template = env.get_template('blog.jinja2')

    contexts = []
    for post in posts:
        context = post.copy()
        if context['type'] in (TYPE_TEXT, TYPE_QUOTE):
            context['url'] = FILEPATH.format(**post)
        contexts.append(context)

    filepath = os.path.join(output_dir, 'index.html')
    with open(filepath, 'w') as fp:
        LOG.debug('Before write `%s`', filepath)
        fp.write(template.render(posts=contexts))
    LOG.info('wrote %s', filepath)


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
