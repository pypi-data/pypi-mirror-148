from typing import Optional, TypeVar

from .persisted import MapFn, PathLike, Persisted, no_load, no_save

T = TypeVar("T")


def string_load(fname: str):
    with open(fname, "r", encoding="utf8") as file:
        return file.read()


def string_save(fname: str, current: str):
    with open(fname, "w", encoding="utf8") as file:
        file.write(current)


def as_string(
    fname: PathLike,
    value: T,
    load: bool = True,
    save: bool = True,
    deserial_fn: Optional[MapFn[str, T]] = None,
    serial_fn: Optional[MapFn[T, str]] = None,
):
    return Persisted[str, T](
        fname,
        value,
        load_fn=string_load if load else no_load,
        save_fn=string_save if save else no_save,
        deserial_fn=deserial_fn,
        serial_fn=serial_fn,
    )
