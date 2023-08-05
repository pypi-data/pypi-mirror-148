import functools
import inspect
from typing import Callable, Type, Iterable, TYPE_CHECKING

from .models import FunctionInformation
from .utils import parse_function_information


class _BaseOperationAdditionDecorator:  # noqa
    """
    Base decorator class, that contain all common logic for
    store and work with decorated functions of services classes
    """

    def __init__(self):
        self._classes_funcs_store: dict[str, dict[str, list[FunctionInformation]]] = {}
        self._classes_funcs_store_cache: dict[Type, list[FunctionInformation]] = {}

    def __getattr__(self, operation_name):
        """
        Use getattr to dynamic registration of any operation additions
        """

        def wrapper(func=None, *, priority: int = -1):
            def decorated_func(f):
                self._register_operation_func(operation_name=operation_name, original_function=f, priority=priority)
                return f

            if func is None:
                return decorated_func
            return decorated_func(func)

        return wrapper

    @staticmethod
    def _get_method_class_identifier(method: Callable) -> str:
        class_name = method.__qualname__.split(".")[0]
        return f"{method.__module__}.{class_name}"  # noqa

    @staticmethod
    def _get_class_identifier(class_obj: Type) -> str:
        class_name = class_obj.__qualname__
        return f"{class_obj.__module__}.{class_name}"

    def _get_class_funcs_by_identifier(self, class_identifier: str) -> dict[str, list[FunctionInformation]]:
        if (res := self._classes_funcs_store.get(class_identifier, None)) is None:
            res = self._classes_funcs_store[class_identifier] = {}
        return res

    def _get_class_funcs(self, class_obj) -> dict[str, list[FunctionInformation]]:
        """
        Used in local cases and can be used only for add/edit class funcs,
        but can't handle MRO recursive funcs handling
        """
        identifier = self._get_class_identifier(class_obj)
        return self._get_class_funcs_by_identifier(identifier)

    def _get_class_funcs_by_method(self, method: Callable) -> dict[str, list[FunctionInformation]]:
        """
        Used in local cases and can be used only for add/edit class funcs,
        but can't handle MRO recursive funcs handling
        """
        identifier = self._get_method_class_identifier(method)
        return self._get_class_funcs_by_identifier(identifier)

    def _register_operation_func(self, operation_name: str, original_function: Callable, priority: int):
        operation_name = operation_name.lower()
        funcs_store = self._get_class_funcs_by_method(original_function)
        if operation_name not in funcs_store:
            funcs_store[operation_name] = []
        funcs_list = funcs_store[operation_name]

        func_info = parse_function_information(original_function)
        func_info.priority = priority
        funcs_list.append(func_info)

    def get_class_operation_funcs(self, class_obj, operation_name: str) -> list[FunctionInformation]:
        classes: Iterable[Type] = reversed(inspect.getmro(class_obj))
        result: list[FunctionInformation] = []
        for obj in classes:
            result.extend(self._get_class_funcs(obj).get(operation_name, []))
        return result


# Decorators collection for automatic running pre-operation functions
pre = _BaseOperationAdditionDecorator()

# Decorators collection for automatic running post-operation functions
post = _BaseOperationAdditionDecorator()


if TYPE_CHECKING:
    # defined here to help IDEs and static type checkers only
    def operation(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

else:

    class operation:
        def __init__(self, method):
            self.method = method
            self.operation = None

        def __set_name__(self, owner, name):
            from .operations import Operation, _AsyncOperation

            if inspect.iscoroutinefunction(self.method):
                self.operation = _AsyncOperation(method=self.method, method_class=owner)
            else:
                self.operation = Operation(method=self.method, method_class=owner)

            @functools.wraps(self.method)
            def wrapper(*args, **kwargs):
                return self.operation(*args, **kwargs)

            setattr(owner, name, wrapper)
