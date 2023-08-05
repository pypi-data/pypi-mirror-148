import os
import sys
from contextlib import contextmanager
from functools import partial
from inspect import ismodule
from itertools import chain
from pathlib import Path
from subprocess import check_call, check_output
from typing import List, Type, TypeVar, Union

import isort
from black import Mode, format_file_contents
from black.report import NothingChanged
from sqlalchemy.dialects.postgresql import dialect as postgres_dialect
from yaml import safe_load

from .naming import MAIN_MODULE_NAME, META_MODULE_NAME

LINE_LEN = 119
PRIMITIVE_MODULES = ["builtins", "datetime"]
T = TypeVar("T")
package_root = Path(__file__).parent.parent


def get_cls_defined_in_module(module, parent):
    out = {}
    for poss_cls_name in dir(module):
        cls = getattr(module, poss_cls_name)
        try:
            if parent in cls.mro()[1:]:
                out[poss_cls_name] = cls
        except (AttributeError, TypeError):
            pass
    return out


def get_instances_from_module(module, cls):
    out = {}
    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if isinstance(obj, cls):
            out[obj_name] = obj
    return out


def get_modules_from_module(module, root_name: str):
    out = {}
    for obj_name in dir(module):
        obj = getattr(module, obj_name)
        if ismodule(obj) and obj.__name__.startswith(root_name):
            out[obj_name] = obj
    return out


def is_repo(s):
    return any(map(str(s).startswith, ["git@", "http://", "https://"]))


def git_run(add=(), msg=None, pull=False, push=False, wd=None):
    for k, git_cmd in [
        (add, ["add", *add]),
        (msg, ["commit", "-m", msg]),
        (pull, ["pull"]),
        (push, ["push"]),
    ]:
        if k:
            check_call(["git", *git_cmd], cwd=wd)


def get_git_diffs(staged=False):
    comm = ["git", "diff", "--name-only"]
    if staged:
        comm.append("--cached")
    diffs = check_output(comm)
    return [*filter(None, diffs.decode("utf-8").strip().split("\n"))]


@contextmanager
def cd_into(dirpath: Union[str, Path]):
    wd = os.getcwd()
    os.chdir(dirpath)
    # sys.path.insert(0, str(dirpath))
    reset_src_module()
    try:
        yield
    finally:
        os.chdir(wd)
        # sys.path.pop(0)


def format_code(code_str):
    try:
        mode = Mode(line_length=LINE_LEN)
        blacked = format_file_contents(code_str, fast=True, mode=mode)
    except NothingChanged:
        blacked = code_str

    return isort.code(blacked, profile="black")


def load_named_dict_to_list(
    path: Path,
    cls: Type[T],
    key_name="name",
) -> List[T]:
    return named_dict_to_list(safe_load(path.read_text()) or {}, cls, key_name)


def named_dict_to_list(
    named_dict: dict,
    cls: Type[T],
    key_name="name",
) -> List[T]:
    out = []
    for k, kwargs in named_dict.items():
        out.append(cls(**{key_name: k, **kwargs}))
    return out


def get_dict_factory(key_name: str):
    return partial(_dicfac, att_name=key_name)


def reset_src_module():
    for m_id in filter(
        lambda k: k.startswith(f"{MAIN_MODULE_NAME}.") or (k == MAIN_MODULE_NAME),
        [*sys.modules.keys()],
    ):
        sys.modules.pop(m_id)


def reset_meta_module():
    for m_id in [*sys.modules.keys()]:
        if m_id.startswith(f"{META_MODULE_NAME}."):
            sys.modules.pop(m_id)


def is_type_hint_origin(hint, cls):
    try:
        return hint.__origin__ is cls
    except AttributeError:
        return False


def chainmap(fun, iterable) -> list:
    return [*chain(*map(fun, iterable))]


def is_postgres(engine):
    return isinstance(engine.dialect, postgres_dialect)


def _dicfac(items, att_name):
    return {k: v for k, v in items if v and k != att_name}
