from collections.abc import Callable, MutableMapping, Iterator
from enum import Enum
from typing import TypeVar, Optional, Union, TypeGuard
from warnings import warn

from .types import UNSET, UnSet
from .typing import RegistryKeyProtocol, RegistryKeyConstructorProtocol


__ALL__ = [
    'BaseRegistry',
]


V = TypeVar('V')
K = TypeVar('K')


class _ChangeBehavior(str, Enum):

    IGNORE = 'ignore_changes'
    WARN = 'warn_changes'
    RAISE = 'raise_changes'

    @classmethod
    def ignore_changes(cls, msg: str):
        pass

    @classmethod
    def warn_changes(cls, msg: str):
        warn(msg)

    @classmethod
    def raise_changes(cls, msg: str):
        raise TypeError(msg)

    def report_changes(self, msg: str):
        behavior = getattr(self, self.value)
        return behavior(msg)


class BaseRegistry(MutableMapping[K, V]):

    registry_key_constructor: RegistryKeyConstructorProtocol = NotImplemented
    ChangeBehavior = _ChangeBehavior

    def __init_subclass__(cls, change_behavior: _ChangeBehavior = ChangeBehavior.IGNORE, **kwargs):
        super().__init_subclass__(**kwargs)

        constructor = cls.registry_key_constructor
        if constructor is NotImplemented:
            raise NotImplementedError(f"{cls.__name__} must define a registry_key_constructor")

        if not hasattr(constructor, 'iter_defaults'):
            cls.get_default_by_key = cls._get_default_always        # type: ignore

        cls._report_changes = change_behavior.report_changes        # type: ignore

    def __init__(self, m: Optional[MutableMapping[K, V]] = None, default: V | UnSet = UNSET):
        self._registry = m or dict()
        self._default = default

    def __getitem__(self, registry_key: K) -> V:
        # Check if full definition exists
        return self.get_content_by_key(registry_key)

    def __setitem__(self, registry_key: K, content: V):
        self.set_content_by_key(registry_key, content)

    def __delitem__(self, registry_key: K):
        self._report_changes(f"unregistering {registry_key}")
        del self._registry[registry_key]

    def __iter__(self) -> Iterator[K]:
        return iter(self._registry)

    def __len__(self) -> int:
        return len(self._registry)

    def __repr__(self):
        return f"{self.__class__.__name__}({self._registry!r})"

    @property
    def default(self):
        return self._default

    @default.setter
    def default(self, value: V):
        if self._default is not UNSET and self._report_changes is not self.ChangeBehavior.IGNORE and \
                value != self._default:
            self._report_changes(f"default changed from {self._default} to {value}")
        else:
            self._default = value

    # Alternative implementations for get_default_by_key
    def get_default_by_key(self, registry_key: RegistryKeyProtocol, default: Union[V, UnSet] = UNSET) -> V:
        default_keys = (k for k in registry_key.iter_defaults())
        default_contents = (
            c for c in (
                    self._registry.get(k, UNSET) for k in default_keys  # type: ignore
                    ) if c is not UNSET
            )
        content = next(default_contents, default)

        if content is UNSET:
            raise KeyError(f"{registry_key} (no defaults have been set)")

        return content      # type: ignore

    def _get_default_always(self, registry_key: K, default: Union[V, UnSet] = UNSET) -> V:
        if default is UNSET:
            raise KeyError(f"{registry_key} (no defaults have been set)")

        return default      # type: ignore

    @staticmethod
    def _report_changes(msg: str):
        pass

    # Alternative implementations for setting content
    def set_content_by_key(self, registry_key: K, content: V):
        if self._report_changes is not self.ChangeBehavior.IGNORE:
            existing_content = self._registry.get(registry_key, UNSET)  # type: ignore
            if existing_content is not UNSET and content != existing_content:
                self._report_changes(f"setting existing registration for {registry_key}")
        self._registry[registry_key] = content

    def get_content_by_key(self, registry_key: K, default: V | UnSet = UNSET):
        if default is UNSET:
            default = self.default

        content = self._registry.get(registry_key, UNSET)   # type: ignore

        if content is UNSET:
            content = self.get_default_by_key(registry_key, default=default)  # type: ignore

        return content

    # Easy access via key constructor
    def get_content(
            self,
            *key_args,
            default=UNSET,
            **key_kwargs,
            ) -> V:
        return self.get_content_by_key(
                self.registry_key_constructor(*key_args, **key_kwargs),   # type: ignore
                default=default
            )

    def register_content(
            self,
            content: V,
            *key_args,
            **key_kwargs
            ):
        self.set_content_by_key(
            self.registry_key_constructor(*key_args, **key_kwargs),  # type: ignore
            content
            )

    def register(
            self,
            *key_args,
            **key_kwargs,
            ) -> Callable[[V], V]:

        def decorates(content: V) -> V:
            self.register_content(content, *key_args, **key_kwargs)
            return content

        return decorates
