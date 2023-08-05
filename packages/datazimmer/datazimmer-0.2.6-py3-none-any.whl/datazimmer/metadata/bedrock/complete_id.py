from dataclasses import dataclass
from typing import Generic, Optional, Type

from ...naming import MAIN_MODULE_NAME, META_MODULE_NAME, NS_ID_SEPARATOR
from ...utils import PRIMITIVE_MODULES, T


@dataclass
class CompleteId:
    """bedrock id with a namespace prefix

    namespace/project None means local id
    """

    project: Optional[str]
    namespace: Optional[str]
    obj_id: str

    def absolute_from(self, base: "CompleteIdBase"):
        art, ns = self.project or base.project, self.namespace or base.namespace
        return CompleteId(art, ns, self.obj_id)

    def relative_to(self, base: "CompleteIdBase"):
        nsid = self.namespace
        aid = None if base.project == self.project else self.project
        if (aid is None) and (self.namespace == base.namespace):
            nsid = None
        return CompleteId(aid, nsid, self.obj_id)

    @property
    def datascript_obj_accessor(self):
        pref = self.project and META_MODULE_NAME
        return self._joiner(".", pref)

    @property
    def serialized_id(self):
        return self._joiner(NS_ID_SEPARATOR)

    @property
    def is_local(self):
        return self.namespace is None

    @property
    def module(self):
        elems = [META_MODULE_NAME, self.project, self.namespace]
        return ".".join(elems)

    @property
    def base(self):
        return CompleteIdBase(self.project, self.namespace)

    @classmethod
    def from_serialized_id(cls, id_: str) -> "CompleteId":
        split_id = [None, None, *id_.split(NS_ID_SEPARATOR)]
        return cls(*split_id[-3:])

    @classmethod
    def from_datascript_cls(cls, py_cls: Type) -> "CompleteId":
        return CompleteIdBase.from_cls(py_cls).to_id(py_cls.__name__)

    def _joiner(self, join_str, prefix=None):
        elems = [prefix, self.project, self.namespace, self.obj_id]
        return join_str.join(filter(None, elems))


@dataclass
class CompleteIdBase:
    project: Optional[str]
    namespace: Optional[str]

    def to_id(self, name) -> CompleteId:
        return CompleteId(self.project, self.namespace, name)

    @classmethod
    def from_cls(cls, py_cls, project=None):
        _mod = py_cls.__module__
        if _mod in PRIMITIVE_MODULES:
            return cls(None, None)
        return cls.from_module_name(_mod, project)

    @classmethod
    def from_module_name(cls, module_name, project=None):
        _splitted = module_name.split(".")
        if _splitted[0] == META_MODULE_NAME:
            return cls(*_splitted[1:])
        elif _splitted[0] == MAIN_MODULE_NAME:
            return cls(project, _splitted[1])

    @property
    def import_str(self):
        if self.project:
            return f"import {self.ext_module_name}"
        if self.namespace:
            return f"from . import {self.namespace}"

    @property
    def ext_module_name(self):
        return ".".join([META_MODULE_NAME, self.project, self.namespace])


class CompleteIdOf(Generic[T], CompleteId):
    pass
