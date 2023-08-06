from typing import Optional, TypeVar

from .persisted import MapFn, PathLike, Persisted, no_load, no_save

T = TypeVar("T")


def bytes_load(fname: str):
    with open(fname, "rb") as file:
        return file.read()


def bytes_save(fname: str, current: bytes):
    with open(fname, "wb") as file:
        file.write(current)


def as_bytes(
    fname: PathLike,
    value: T,
    load: bool = True,
    save: bool = True,
    deserial_fn: Optional[MapFn[bytes, T]] = None,
    serial_fn: Optional[MapFn[T, bytes]] = None,
):
    return Persisted[bytes, T](
        fname,
        value,
        load_fn=bytes_load if load else no_load,
        save_fn=bytes_save if save else no_save,
        deserial_fn=deserial_fn,
        serial_fn=serial_fn,
    )
