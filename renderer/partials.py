from logging import getLogger
from os import path

log = getLogger(__name__)


def render(env, output_dir):
    render_about(env, output_dir)
    render_placeholders(env, output_dir)
    render_search(env, output_dir)


def render_about(env, output_dir):
    try:
        filepath = path.relpath(path.join(output_dir, 'about.html'))
        template = env.get_template('_about.html')
        with open(filepath, 'w') as fp:
            fp.write(template.render())
            log.info('OK {}'.format(filepath))
    except Exception as err:
        log.fatal('Could not process {}:'.format(filepath), err)
        raise err


def render_placeholders(env, output_dir):
    for route in ('about', 'blog', 'portfolio'):
        filepath = path.relpath(path.join(output_dir, '{}.loading.html'.format(route)))
        try:
            template = env.get_template('_{}.loading.html'.format(route))
            log.debug('render_placeholders:Before render/write `{}`'.format(route))
            with open(filepath, 'w') as fp:
                fp.write(template.render())
                log.info('OK {}'.format(path.basename(filepath)))
        except Exception as err:
            log.fatal('Could not process {}:'.format(filepath), err)
            raise err


def render_search(env, output_dir):
    try:
        filepath = path.relpath(path.join(output_dir, 'search.html'))
        template = env.get_template('_search.html')
        with open(filepath, 'w') as fp:
            fp.write(template.render())
            log.info('OK {}'.format(filepath))
    except Exception as err:
        log.fatal('Could not process {}:'.format(filepath), err)
        raise err
