import glob
import logging
import os
import re
import sys
import xml.etree.ElementTree as etree

DTD_PREAMBLE = """\
<!DOCTYPE portfolio-item [
<!ENTITY quot    "&#34;">
<!ENTITY amp     "&#38;#38;">
<!ENTITY lt      "&#38;#60;">
<!ENTITY gt      "&#62;">
<!ENTITY apos    "&#39;">
<!ENTITY ndash   "&#8211;">
<!ENTITY mdash   "&#8212;">
<!ENTITY lsquo   "&#8216;">
<!ENTITY rsquo   "&#8217;">
<!ENTITY ldquo   "&#8220;">
<!ENTITY rdquo   "&#8221;">
]>
"""
TYPE_PHOTOSHOP = 'photoshop'
TYPE_UI = 'ui'

log = logging.getLogger(__name__)


def clean(output_dir):
    for filepath in glob.glob(os.path.join(output_dir, 'portfolio/*.html')):
        log.info('clean %s', os.path.relpath(filepath))
        os.unlink(filepath)


def render(env, xml_dir, output_dir):
    creative_works = []
    failures = []

    for filepath in glob.glob(os.path.join(xml_dir, '*.xml')):
        filepath = os.path.relpath(filepath)
        try:
            creative_work = _deserialize_creative_work(filepath)
            creative_works.append(creative_work)
        except ExtractionError as err:
            log.error('Failed on {}\n    {}'.format(filepath, err))
            _dump_node(err.node)
            failures.append(filepath)
        except Exception as err:
            log.fatal('Could not process `{}`\n\t{}: {}'.format(filepath, err.__class__.__name__, err))
            raise err

    creative_works = sorted(creative_works, reverse=True, key=lambda d: d['circa'])
    _render_index(env, creative_works, output_dir)

    # Report card
    if failures:
        log.warn('*** {} failures: {}'.format(len(failures), ', '.join(failures)))


################################################################################

#
# Internals
#

def _deserialize_creative_work(filepath):
    xml = _prepare_xml(filepath)
    try:
        document = etree.fromstring(xml)

        work_type = document.get('type')
        if work_type == TYPE_PHOTOSHOP:
            record = _generate_photoshop_work(document)
            _validate_photoshop_work(record)
        elif work_type == TYPE_UI:
            record = _generate_ui_work(document)
            _validate_ui_work(record)
        else:
            raise ExtractionError('Invalid `type` "{}"'.format(work_type), document)

        log.info('OK {}'.format(filepath))
        return record
    except etree.ParseError as err:
        log.fatal(err)
        _dump_xml(xml)
        raise err


def _dump_node(node: etree.Element, indent=' ' * 4):
    return _dump_xml(etree.tostring(node).decode(), indent)


def _dump_xml(xml, indent=' ' * 4):
    print(indent + ('-' * 80))
    for line_number, line in enumerate(xml.splitlines()):
        print('{0}{1:>3} | {2}'.format(indent, line_number + 1, line))
    print(indent + ('-' * 80))
    print()
    sys.stdout.flush()


def _extract_artifacts(e: etree.Element):
    nodes = e.findall('artifact')
    if not nodes:
        raise ExtractionError('Missing `artifact` element', e)
    return [dict(n.items()) for n in nodes]


def _extract_brand(e: etree.Element):
    value = e.findtext('brand')
    if not value:
        raise ExtractionError('Missing `brand` element', e)
    return value


def _extract_category(e: etree.Element):
    return e.findtext('category')


def _extract_circa(e: etree.Element):
    value = e.findtext('circa')
    if not value:
        raise ExtractionError('Missing `circa` element', e)
    try:
        return int(value)
    except TypeError:
        raise ExtractionError('Invalid `circa` value "{}"'.format(value), e)


def _extract_client(e: etree.Element):
    value = e.findtext('client')
    if not value:
        raise ExtractionError('Missing `client` element', e)
    return value


def _extract_id(e: etree.Element):
    return re.sub(r'\W', '-', _extract_name(e).lower())


def _extract_links(e: etree.Element):
    nodes = e.findall('link')
    links = []
    for node in nodes:
        try:
            links.append({
                'artifactIndex': int(node.get('artifact-index')),
                'label': node.get('label')
            })
        except:
            raise ExtractionError('Malformed `link` element', e)
    return links


def _extract_name(e: etree.Element):
    value = e.findtext('name')
    if not value:
        raise ExtractionError('Missing `name` element', e)
    return value


def _extract_narratives(e: etree.Element):
    nodes = e.findall('narrative')
    if not nodes:
        raise ExtractionError('Missing `narrative` element', e)
    narratives = []
    for node in nodes:
        narrative = {}

        narrative['links'] = _extract_links(node)
        narrative['mural'] = node.get('mural', None)

        # Remove link tags from emitted markup
        for link_node in node.findall('link'):
            node.remove(link_node)

        narrative['markup'] = ''.join([etree.tostring(n).decode().strip() for n in node])
        narratives.append(narrative)
    return narratives


def _extract_primary_link(e: etree.Element):
    links = _extract_links(e)
    if not links:
        raise ExtractionError('Missing primary `link` element', e)
    return links[0]


def _extract_primary_artifact(e: etree.Element):
    artifact, = _extract_artifacts(e)
    if not artifact:
        raise ExtractionError('Missing primary `artifact` element', e)
    return artifact


def _extract_summary(e: etree.Element):
    value = e.findtext('summary')
    if not value:
        raise ExtractionError('Missing `summary` element', e)
    return value.strip()


def _extract_tags(e: etree.Element):
    return [node.text for node in e.findall('tag')]


def _extract_technologies(e: etree.Element):
    value = e.findtext('technologies')
    if not value:
        raise ExtractionError('Missing `technologies` element', e)
    return value.strip()


def _extract_type(e: etree.Element):
    return e.get('type')


def _generate_photoshop_work(e: etree.Element):
    return {
        'id': _extract_id(e),
        'type': _extract_type(e),
        'name': _extract_name(e),
        'tags': _extract_tags(e),
        'circa': _extract_circa(e),
        'summary': _extract_summary(e),
        'artifact': _extract_primary_artifact(e)
    }


def _generate_ui_work(e: etree.Element):
    return {
        'id': _extract_id(e),
        'type': _extract_type(e),
        'category': _extract_category(e),
        'name': _extract_name(e),
        'link': _extract_primary_link(e),
        'tags': _extract_tags(e),
        'circa': _extract_circa(e),
        'narratives': _extract_narratives(e),
        'summary': _extract_summary(e),
        'technologies': _extract_technologies(e),
        'artifacts': _extract_artifacts(e),
        'brand': _extract_brand(e),
        'client': _extract_client(e)
    }


def _prepare_xml(filepath):
    log.debug('READ `{0}`'.format(filepath))
    with open(filepath) as fp:
        return DTD_PREAMBLE + fp.read()


def _render_index(env, creative_works, output_dir):
    template = env.get_template('_portfolio.index.jinja2')

    filepath = os.path.relpath(os.path.join(output_dir, 'portfolio/index.html'))

    ui_works = list(filter(lambda d: d['type'] == TYPE_UI, creative_works))
    photoshop_works = list(filter(lambda d: d['type'] == TYPE_PHOTOSHOP, creative_works))
    with open(filepath, 'w') as fp:
        fp.write(template.render(
            ui_works=ui_works,
            photoshop_works=photoshop_works,
        ))
        log.info('OK {}'.format(filepath))


def _validate_photoshop_work(record: dict):
    # TODO -- has primary artifact
    pass


def _validate_ui_work(record: dict):
    # TODO -- Primary link refers to an existing artifact index
    # TODO -- All narratives refer to existing artifact indices
    pass


class ExtractionError(Exception):
    def __init__(self, message, node: etree.Element):
        self.message = message
        self.node = node

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.message)


class ValidationError(Exception):
    def __init__(self, message, record):
        self.message = message
        self.record = record

    def __str__(self):
        return '{}: {}'.format(self.__class__.__name__, self.message)
