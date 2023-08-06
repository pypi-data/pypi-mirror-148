import logging
import os
import os.path
import pathlib
from asyncio import Lock
from types import TracebackType
from typing import Any, Callable, Generic, Optional, Type, TypeVar, Union, cast

S = TypeVar("S")
T = TypeVar("T")

PathLike = Union[str, pathlib.Path]
LoadFn = Callable[[str], T]
SaveFn = Callable[[str, T], None]
MapFn = Callable[[S], T]


LOG = logging.getLogger(__name__)


class SkipLoad(Exception):
    pass


def identity(x: Any) -> Any:
    return x


def no_load(fname: str):
    raise SkipLoad()


def no_save(fname: str, value: Any):
    pass


class Persisted(Generic[S, T]):
    def __init__(
        self,
        fname: PathLike,
        initial: T,
        load_fn: LoadFn[S],
        save_fn: SaveFn[S],
        deserial_fn: Optional[MapFn[S, T]] = None,
        serial_fn: Optional[MapFn[T, S]] = None,
    ) -> None:
        self.fname = str(fname)
        self.value = initial

        self.lock = Lock()
        self.saved = 0.0

        self.load_fn = load_fn
        self.deserial_fn = deserial_fn if deserial_fn else identity
        self.serial_fn = serial_fn if serial_fn else identity
        self.save_fn = save_fn

        self.load()

    def load(self) -> None:
        try:
            modified = os.stat(self.fname).st_mtime
        except FileNotFoundError:
            return

        if modified <= self.saved:
            return

        LOG.info(
            "loaded %s because state (%s) < current (%s)",
            self.fname,
            self.saved,
            modified,
        )
        try:
            self.value = cast(T, self.deserial_fn(self.load_fn(self.fname)))
        except SkipLoad:
            pass
        self.saved = modified

    def save(self) -> None:
        self.save_fn(self.fname, self.serial_fn(self.value))
        self.saved = os.stat(self.fname).st_mtime

    def __enter__(self) -> T:
        return self.get()

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.save()

    async def __aenter__(self) -> T:
        return await self.acquire()

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        self.release()

    def is_invalidated(self, time: float) -> bool:
        self.load()
        return self.saved > time

    def get(self) -> T:
        self.load()
        return self.value

    def get_time(self) -> float:
        return self.saved

    def set(self, value: T) -> None:
        self.value = value
        self.save()

    def replace(self, value: T) -> None:
        self.value = value

    async def acquire(self) -> T:
        await self.lock.acquire()
        self.load()
        return self.value

    def release(self, value: Optional[T] = None) -> None:
        if value is not None:
            self.value = value
            self.save()
        self.lock.release()
