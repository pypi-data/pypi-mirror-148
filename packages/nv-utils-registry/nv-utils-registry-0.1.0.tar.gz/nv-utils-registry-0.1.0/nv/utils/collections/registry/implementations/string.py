from collections.abc import Iterable
from functools import cached_property

from ..core import BaseRegistry, V


__ALL__ = ['StrPathRegistryKey', 'StrPathRegistry', 'StrRegistry']


class StrPathRegistryKey:
    PATH_SEPARATOR = '/'
    ALL_PATHS = '*'

    def __init__(self, path: str):
        self._path = self._clean_path(path)

    def __str__(self):
        return self.path

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._path}')"

    def __hash__(self):
        return hash(self._path)

    @property
    def path(self):
        return self._path or self.PATH_SEPARATOR

    @cached_property
    def all_children(self):
        return self.__class__(f"{self._path}{self.PATH_SEPARATOR}{self.ALL_PATHS}")

    @cached_property
    def as_components(self):
        return self._path.split(self.PATH_SEPARATOR)

    def iter_upwards(self, include_self=True) -> Iterable['StrPathRegistryKey']:
        upward_path = self.as_components if include_self else self.as_components[:-1]
        while upward_path:
            yield self.__class__(self.PATH_SEPARATOR.join(upward_path))
            upward_path = upward_path[:-1]

    def iter_defaults(self) -> Iterable['StrPathRegistryKey']:
        for parent in self.iter_upwards(include_self=False):
            yield parent.all_children

    def _clean_path(self, path: str) -> str:
        if path == self.PATH_SEPARATOR or not path:
            # root path
            return ''

        if not path.startswith(self.PATH_SEPARATOR):
            path = f"{self.PATH_SEPARATOR}{path}"

        if path.endswith(self.PATH_SEPARATOR):
            path = path[:-1]

        return path


class StrPathRegistry(BaseRegistry[StrPathRegistryKey, V]):
    registry_key_constructor = StrPathRegistryKey


class StrRegistry(BaseRegistry[str, V]):
    registry_key_constructor = str
