import importlib
from pathlib import Path
from typing import Callable
from typhoon.introspection.introspect_local_project import get_local_function


def get_function(function_module: str, function_submodule: str, function_name: str) -> Callable:
    from typhoon.deployment.packaging import local_typhoon_path
    if function_module == 'functions':
        return get_local_function(function_submodule, function_name)
    elif function_module == 'typhoon':
        module_path = Path(local_typhoon_path())/f'contrib/functions/{function_submodule}.py'
        spec = importlib.util.spec_from_file_location(module_path.stem, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module.__getattribute__(function_name)
    else:
        raise ValueError(f'Unsupported function_module {function_module}')
