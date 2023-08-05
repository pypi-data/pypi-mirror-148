import functools
import inspect
from typing import Callable, Type, Any, Optional

from .arguments import ArgumentsStore, Argument
from .models import FunctionInformation, FunctionArgInfo
from .utils import parse_function_information


class OperationBase:
    def __init__(self, method: Callable, method_class: Type):
        functools.update_wrapper(self, method)
        self.method: FunctionInformation = parse_function_information(method)
        self.method_class: Type = method_class

    @property
    def operation_name(self) -> str:
        return self.method.name

    @property
    def operation_method(self) -> str:
        return f"{self.method_class.__name__}.{self.method.function_object.__name__}"

    def __call__(self, *args, **kwargs):
        return self.method.function_object(*args, **kwargs)


class Operation(OperationBase):
    # Setup and clean up method

    def __init__(self, *args, **kwargs):
        from .decorators import pre, post

        super(Operation, self).__init__(*args, **kwargs)

        self._pre_operation_funcs: list[FunctionInformation] = pre.get_class_operation_funcs(
            class_obj=self.method_class, operation_name=self.operation_name
        )
        self._post_operation_funcs: list[FunctionInformation] = post.get_class_operation_funcs(
            class_obj=self.method_class, operation_name=self.operation_name
        )

        # Attributes that changes on each operation call
        self._operation_self_obj = None
        self.initial_arguments_store: Optional[ArgumentsStore] = None
        self.arguments_store: Optional[ArgumentsStore] = None

    def _setup_operation_state(self, *args, **kwargs):
        try:
            self._setup_operation_self_obj(args[0])
        except IndexError:
            raise ValueError(f'Cant extract "self" for method {self.operation_method} on preparing of operation')
        self._setup_operation_args_stores(args[1:], **kwargs)

    def _clean_up_operation_state(self):
        self._clean_up_operation_args_stores()
        self._clean_up_operation_self_obj()

    def _setup_operation_self_obj(self, operation_self_obj) -> None:
        self._operation_self_obj = operation_self_obj

    def _clean_up_operation_self_obj(self) -> None:
        self._operation_self_obj = None

    def _setup_operation_args_stores(self, *args, **kwargs):
        self.initial_arguments_store = ArgumentsStore(operation_args_dict=kwargs, immutable=True)
        self.arguments_store = ArgumentsStore(operation_args_dict=kwargs)

    def _clean_up_operation_args_stores(self):
        self.initial_arguments_store = None
        self.arguments_store = None

    # Core logic
    def __call__(self, *args, **kwargs):
        self._setup_operation_state(*args, **kwargs)

        for additional_func in self._pre_operation_funcs:
            self._execute_function(additional_func)
        result = self._execute_function(self.method)
        for additional_func in self._post_operation_funcs:
            self._execute_function(additional_func)

        self._clean_up_operation_state()
        return result

    def _execute_function(self, func_info: FunctionInformation) -> Any:
        args = self._get_args_for_func(func_info)
        return func_info.function_object(self._operation_self_obj, **args)

    def _get_arg_value_for_func_by_arg_info(self, arg_info: FunctionArgInfo) -> Any:
        if arg_info.type is not None and issubclass(arg_info.type, Operation):
            return self
        elif not isinstance(arg_info.default_value, Argument):
            value = (
                self.arguments_store[arg_info.name] if arg_info.name in self.arguments_store else arg_info.default_value
            )
        else:
            argument_metadata_obj: Argument = arg_info.default_value
            args_store_to_use: ArgumentsStore = (
                self.arguments_store if not argument_metadata_obj.from_initial_args else self.initial_arguments_store
            )
            arg_name_in_store = argument_metadata_obj.from_name or arg_info.name
            value = (
                args_store_to_use[arg_name_in_store]
                if arg_name_in_store in args_store_to_use
                else argument_metadata_obj.default_value
            )
            if argument_metadata_obj.transformer is not None:
                value = argument_metadata_obj.transformer(value)

        return value

    def _get_args_for_func(self, func_info: FunctionInformation) -> dict[str, Any]:
        args = {}
        for arg_name, arg_info in func_info.args.items():
            if arg_name in ["self", "kwargs"]:
                continue
            value = self._get_arg_value_for_func_by_arg_info(arg_info=arg_info)
            if value is Ellipsis:
                continue
            args[arg_name] = value
        if func_info.receives_all_kwargs:
            # add all arguments that not been already added
            for arg_name, value in self.arguments_store.items():
                args[arg_name] = value
        return args


class _AsyncOperation(Operation):
    async def __call__(self, *args, **kwargs):
        self._setup_operation_state(*args, **kwargs)

        for additional_func in self._pre_operation_funcs:
            await self._execute_function(additional_func)
        result = await self._execute_function(self.method)
        for additional_func in self._post_operation_funcs:
            await self._execute_function(additional_func)

        self._clean_up_operation_state()
        return result

    async def _execute_function(self, func_info: FunctionInformation) -> Any:
        args = self._get_args_for_func(func_info)
        if inspect.iscoroutinefunction(func_info.function_object):
            return await func_info.function_object(self._operation_self_obj, **args)
        else:
            return func_info.function_object(self._operation_self_obj, **args)
