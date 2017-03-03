import glob
import logging
import os

log = logging.getLogger(__name__)


def render(env, output_dir):
    render_about(env, output_dir)
    render_error_pages(env, output_dir)
    render_placeholders(env, output_dir)
    render_search(env, output_dir)


def render_about(env, output_dir):
    _render(env,
            template='_about.jinja2',
            output=os.path.join(output_dir, 'about.html'))


def render_error_pages(env, output_dir):
    _render(env,
            template='_404.jinja2',
            output=os.path.join(output_dir, '404.html'))


def render_placeholders(env, output_dir):
    for route in ('about', 'blog', 'portfolio'):
        filepath = os.path.join(output_dir, '_{}_loading.html'.format(route))
        try:
            template = env.get_template('_{}.loading.jinja2'.format(route))
            log.debug('render_placeholders:Before render/write `{}`'.format(route))
            with open(filepath, 'w') as fp:
                fp.write(template.render())
                log.info('OK {}'.format(os.path.basename(filepath)))
        except Exception as err:
            log.fatal('Could not process %s:', filepath, err)
            raise err


def render_search(env, output_dir):
    _render(env,
            template='_search.jinja2',
            output=os.path.join(output_dir, 'search.html'))


###############################################################################

#
# Internals
#

def _render(env, *, template: str, output: str):
    filepath = os.path.relpath(output)
    try:
        template = env.get_template(template)
        with open(filepath, 'w') as fp:
            fp.write(template.render())
            log.info('OK {}'.format(filepath))
    except Exception as err:
        log.fatal('Could not process %s: %s', filepath, err)
        raise err
