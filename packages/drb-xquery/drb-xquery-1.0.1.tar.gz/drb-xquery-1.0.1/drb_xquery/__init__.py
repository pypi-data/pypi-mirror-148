from .drb_xquery import DrbXQuery

from . import _version

__version__ = _version.get_versions()['version']

from .drb_xquery_context import DynamicContext

del _version

__all__ = [
    'DrbXQuery', 'DynamicContext'
]
