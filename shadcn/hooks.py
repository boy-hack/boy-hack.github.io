import mkdocs.plugins
from filters import (
    active_section,
    first_page,
    iconify,
    parse_author,
    setattribute,
    timestamp_to_date,
)
import logging
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.structure.nav import Navigation, Section
from mkdocs.config.base import Config
from mkdocs.structure.files import Files
import re

log = logging.getLogger('mkdocs')


@mkdocs.plugins.event_priority(-50)
def on_env(env, /, *, config, files):
    # custom jinja2 filter
    log.info("on_env")
    env.filters["setattribute"] = setattribute
    env.filters["iconify"] = iconify
    env.filters["parse_author"] = parse_author
    env.filters["active_section"] = active_section
    env.filters["first_page"] = first_page
    env.filters["timestamp_to_date"] = timestamp_to_date
    return env
