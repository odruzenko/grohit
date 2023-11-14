from importlib import import_module


def load_class_by_name(clazz: str) -> type:
    module_path, class_name = clazz.rsplit(".", 1)
    module = import_module(module_path)
    return getattr(module, class_name)
