from typing import Protocol, Iterable, Hashable


class RegistryKeyProtocol(Hashable, Protocol):
    def iter_defaults(self) -> Iterable['RegistryKeyProtocol']: ...


class RegistryKeyConstructorProtocol(Hashable, Protocol):
    def __call__(self, *args, **kwargs) -> RegistryKeyProtocol: ...
