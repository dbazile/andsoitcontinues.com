import glob
import logging
import os

LOG = logging.getLogger(__name__)


def clean(output_dir):
    for filepath in glob.glob(os.path.join(output_dir, '*.html')):
        LOG.info('clean %s', filepath)
        os.unlink(filepath)


def render(env, output_dir):
    render_about(env, output_dir)
    render_error_pages(env, output_dir)
    render_loading_placeholders(env, output_dir)
    render_search(env, output_dir)


def render_about(env, output_dir):
    _render(env,
            template='about.jinja2',
            output=os.path.join(output_dir, 'about.html'))


def render_error_pages(env, output_dir):
    _render(env,
            template='404.jinja2',
            output=os.path.join(output_dir, '404.html'))


def render_loading_placeholders(env, output_dir):
    for route in ('about', 'blog', 'portfolio'):
        filepath = os.path.join(output_dir, '.{}.html'.format(route))
        try:
            template = env.get_template('{}__loading.jinja2'.format(route))
            LOG.debug('Before render/write `{}`'.format(route))
            with open(filepath, 'w') as fp:
                fp.write(template.render())
                LOG.info('wrote %s', filepath)
        except Exception as err:
            LOG.fatal('Could not process %s:', filepath, err)
            raise err


def render_search(env, output_dir):
    _render(env,
            template='search.jinja2',
            output=os.path.join(output_dir, 'search.html'))


###############################################################################

#
# Internals
#

def _render(env, *, template: str, output: str):
    try:
        template = env.get_template(template)
        with open(output, 'w') as fp:
            fp.write(template.render())
            LOG.info('wrote {}'.format(output))
    except Exception as err:
        LOG.fatal('Could not process %s: %s', output, err)
        raise err
