"""
WiP.

Soon.
"""

# region [Imports]

import os
import re
import sys
import json
import queue
import math
import base64
import pickle
import random
import shelve
import dataclasses
import shutil
import asyncio
import logging
import sqlite3
import platform
import importlib
import subprocess
import inspect

from time import sleep, process_time, process_time_ns, perf_counter, perf_counter_ns
from io import BytesIO, StringIO
from abc import ABC, ABCMeta, abstractmethod
from copy import copy, deepcopy
from enum import Enum, Flag, auto, unique
from time import time, sleep
from pprint import pprint, pformat
from pathlib import Path
from string import Formatter, digits, printable, whitespace, punctuation, ascii_letters, ascii_lowercase, ascii_uppercase
from timeit import Timer
from typing import TYPE_CHECKING, Union, Callable, Iterable, Optional, Mapping, Any, IO, TextIO, BinaryIO, Hashable, Generator, Literal, TypeVar, TypedDict, AnyStr
from zipfile import ZipFile, ZIP_LZMA
from datetime import datetime, timezone, timedelta
from tempfile import TemporaryDirectory
from textwrap import TextWrapper, fill, wrap, dedent, indent, shorten
from functools import wraps, partial, lru_cache, singledispatch, total_ordering, cached_property
from importlib import import_module, invalidate_caches
from contextlib import contextmanager, asynccontextmanager, nullcontext, closing, ExitStack, suppress
from statistics import mean, mode, stdev, median, variance, pvariance, harmonic_mean, median_grouped
from collections import Counter, ChainMap, deque, namedtuple, defaultdict
from urllib.parse import urlparse
from importlib.util import find_spec, module_from_spec, spec_from_file_location
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from importlib.machinery import SourceFileLoader
from weakref import WeakMethod, WeakSet, WeakKeyDictionary, WeakValueDictionary, ref
if TYPE_CHECKING:
    from weakref import ReferenceType
# endregion[Imports]

# region [TODO]


# endregion [TODO]

# region [Logging]


# endregion[Logging]

# region [Constants]

THIS_FILE_DIR = Path(__file__).parent.absolute()

# endregion[Constants]


def ref_or_weakmethod(item, callback: Callable[["ReferenceType"], Any]) -> "ReferenceType":
    if inspect.ismethod(item):
        return WeakMethod(item, callback)
    return ref(item, callback)


class MethodEnabledWeakSet(WeakSet):

    def add(self, item) -> None:
        if self._pending_removals:
            self._commit_removals()
        ref_item = ref_or_weakmethod(item, self._remove)
        self.data.add(ref_item)


def make_repr(instance: object, attr_names: Union[Callable, Iterable[str]] = None, exclude_none: bool = True) -> str:
    attr_names = attr_names or vars
    if callable(attr_names):
        attr_dict = attr_names(instance)
    else:
        attr_dict = {}
        for name in attr_names:
            try:
                attr_value = getattr(instance, name)
                if callable(attr_value):
                    attr_value = attr_value()
            except Exception as e:

                attr_value = f"<{e.__class__.__name__}>"
            attr_dict[name] = attr_value

    if exclude_none is True:
        attr_dict = {k: v for k, v in attr_dict.items() if v is not None}

    return f"{instance.__class__.__name__}(" + ', '.join(f"{k}={v!r}" for k, v in attr_dict.items()) + ')'

# TODO: Unfinished


class CachedClassProperty:
    def __init__(self, fget=None, doc=None):
        self.fget = fget
        if doc is None and fget is not None:
            doc = fget.__doc__
        self.__doc__ = doc
        self._name = ""

    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError(f'unreadable attribute {self._name}')
        return self.fget(obj)


# region[Main_Exec]
if __name__ == '__main__':
    pass

# endregion[Main_Exec]
