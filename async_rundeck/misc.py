from typing import Any


def import_doc(proto_func: Any) -> Any:
    def _(fn: Any):
        fn.__doc__ = proto_func.__doc__
        return fn

    return _
