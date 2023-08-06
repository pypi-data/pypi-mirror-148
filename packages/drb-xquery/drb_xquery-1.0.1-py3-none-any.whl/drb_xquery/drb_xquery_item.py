from typing import Dict, Tuple, Any, List, Optional

from drb import DrbNode, AbstractNode
from drb.exceptions import DrbNotImplementationException, DrbException
from drb.path import ParsedPath


class DrbXqueryItem(AbstractNode):

    def __init__(self, parent: DrbNode, name: str, namespace_uri: str):
        super().__init__()
        self._attributes: Dict[Tuple[str, str], Any] = {}
        self._name = name
        self._namespace_uri = namespace_uri
        self._parent = parent
        self._children: List[DrbNode] = []
        self._path = None
        self._value = None
        self.order_elt = []

    @property
    def parent(self) -> Optional[DrbNode]:
        return self._parent

    @property
    def path(self) -> ParsedPath:
        return self._path

    @property
    def name(self) -> str:
        return self._name

    @property
    def namespace_uri(self) -> Optional[str]:
        return self._namespace_uri

    @property
    def value(self) -> Optional[Any]:
        return self._value

    @property
    def attributes(self) -> Dict[Tuple[str, str], Any]:
        return self._attributes

    def get_attribute(self, name: str, namespace_uri: str = None) -> Any:
        key = (name, namespace_uri)
        if key in self.attributes.keys():
            return self.attributes[key]
        raise DrbException(f'Attribute not found name: {name}, '
                           f'namespace: {namespace_uri}')

    def add_attribute(self, name: str, value: any, namespace_uri: str = None):
        key = (name, namespace_uri)
        self.attributes[key] = value

    def set_attribute(self, attributes: dict):
        self._attributes = attributes

    def set_value(self, value: Any):
        self._value = value

    @property
    def children(self) -> List[DrbNode]:
        return self._children

    def has_impl(self, impl: type) -> bool:
        return False

    def get_impl(self, impl: type, **kwargs) -> Any:
        raise DrbNotImplementationException(f'no {impl} '
                                            f'implementation found')

    def append_child(self, node: DrbNode) -> None:
        self._children.append(node)

    def close(self):
        pass

    def get_named_child_list(self, name: str, namespace_uri: str = None) -> \
            List[DrbNode]:
        """
        Retrieves one or more children via its given name and its namespace.

        Parameters:
            name (str): child name
            namespace_uri (str): child namespace URI (default: None)
        Returns:
            List[DrbNode] - requested children
        Raises:
            TypeError: if item is not an int or a slice
            IndexError: if item is out of range of found children
            DrbException: if no child following given criteria is found
        """
        if self.namespace_aware or namespace_uri is not None:
            named_children = [x for x in self.children if x.name == name
                              and x.namespace_uri == namespace_uri]
        else:
            named_children = [x for x in self.children if x.name == name]
        if len(named_children) <= 0:
            raise DrbException(f'No child found having name: {name} and'
                               f' namespace: {namespace_uri}')
        return named_children

    def __eq__(self, other):
        if self.name != other.name:
            return False
        if self.namespace_uri != other.namespace_uri:
            return False
        if self.value != other.value:
            return False

        return True

    def __ne__(self, other):
        """Overrides the default implementation (unnecessary in Python 3)"""
        return not self.__eq__(other)
