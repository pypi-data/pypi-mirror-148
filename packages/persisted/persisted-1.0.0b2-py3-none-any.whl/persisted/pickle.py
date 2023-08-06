import pickle
from typing import Any, TypeVar

from .persisted import PathLike, Persisted, no_load, no_save

T = TypeVar("T")


def pickle_load(fname: str):
    with open(fname, "rb") as file:
        return pickle.load(file)


def pickle_save(fname: str, current: Any):
    with open(fname, "wb") as file:
        pickle.dump(current, file)


def as_pickle(
    fname: PathLike,
    value: T,
    load: bool = True,
    save: bool = True,
) -> Persisted[T, T]:
    return Persisted[T, T](
        fname,
        value,
        load_fn=pickle_load if load else no_load,
        save_fn=pickle_save if save else no_save,
    )
