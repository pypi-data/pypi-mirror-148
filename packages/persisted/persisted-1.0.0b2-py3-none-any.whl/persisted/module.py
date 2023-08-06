import importlib
import logging
from types import ModuleType
from typing import Optional, TypeVar, cast

from .persisted import LoadFn, Persisted, no_save

S = TypeVar("S")
T = TypeVar("T")


def module_reload(
    module: ModuleType,
    value: T,
    path: Optional[str],
) -> LoadFn[T]:
    if path:

        def reload(fname: str) -> T:
            try:
                importlib.reload(module)
            except KeyboardInterrupt:
                raise
            except:
                logging.getLogger(__name__).warning(
                    "reloading module %s failed",
                    module.__name__,
                    exc_info=True,
                )

            return cast(T, getattr(module, path))

    else:

        def reload(fname: str) -> T:
            try:
                importlib.reload(module)
            except KeyboardInterrupt:
                raise
            except:
                logging.getLogger(__name__).warning(
                    "reloading module %s failed",
                    module.__name__,
                    exc_info=True,
                )

            return value

    return reload


def as_module(value: T) -> Persisted[T, T]:
    path: Optional[str]

    if isinstance(value, ModuleType):
        module = value
        path = None
    else:
        name = value.__module__
        module = importlib.import_module(name)
        path = value.__qualname__

    fname = module.__file__
    assert fname is not None
    return Persisted[T, T](
        fname,
        value,
        load_fn=module_reload(module, value, path),
        save_fn=no_save,
    )
