import functools
import inspect
from typing import Callable, Type, Any, Optional

from .arguments import ArgumentsStore, Argument
from ._models import FunctionInformation, FunctionArgInfo
from ._utils import parse_function_information


class _OperationBase:
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


class Operation(_OperationBase):
    # Setup and clean up method

    def __init__(self, *args, exception_handlers_mapping: Optional[dict[Type, Callable]] = None, **kwargs):

        super(Operation, self).__init__(*args, **kwargs)

        self._transactions_manager = OperationTransactionManager(exception_handlers_mapping=exception_handlers_mapping)
        # Attributes that changes on each operation call
        self._operation_self_obj = None
        self.initial_arguments_store: Optional[ArgumentsStore] = None
        self.arguments_store: Optional[ArgumentsStore] = None
        self._executed_functions: list[FunctionInformation] = []

    @property
    def executed_functions(self) -> list[FunctionInformation]:
        return self._executed_functions

    def _setup_operation_state(self, *args, **kwargs):
        try:
            self._setup_operation_self_obj(args[0])
        except IndexError:
            raise ValueError(f'Cant extract "self" for method {self.operation_method} on preparing of operation')
        self._load_pre_and_post_operation_func()
        self._setup_operation_args_stores(args[1:], **kwargs)
        self._executed_functions: list[FunctionInformation] = []

    def _clean_up_operation_state(self):
        self._executed_functions: list[FunctionInformation] = []
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

    def _load_pre_and_post_operation_func(self):
        from .decorators import pre, post

        self._pre_operation_funcs: list[FunctionInformation] = pre.get_additional_operation_funcs(
            operation_owner_class=self.method_class, operation_name=self.operation_name
        )
        self._post_operation_funcs: list[FunctionInformation] = post.get_additional_operation_funcs(
            operation_owner_class=self.method_class, operation_name=self.operation_name
        )

    # Core logic
    def __call__(self, *args, **kwargs):
        try:
            return self._main_pipeline(*args, **kwargs)
        except Exception as e:
            result = self._transactions_manager.handle_exception(e, self)
            if isinstance(result, Exception):
                raise e
            return result

    def _main_pipeline(self, *args, **kwargs) -> Any:
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
        self._executed_functions.append(func_info)
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
            if argument_metadata_obj.validators is not None:
                for validator in argument_metadata_obj.validators:
                    value = validator(value)

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
                if arg_name in ["self", "kwargs"]:
                    continue
                args[arg_name] = value
        return args


class _AsyncOperation(Operation):
    async def __call__(self, *args, **kwargs):
        try:
            return await self._main_pipeline(*args, **kwargs)
        except Exception as e:
            result = await self._transactions_manager.ahandle_exception(e, self)
            if isinstance(result, Exception):
                raise e
            return result

    async def _main_pipeline(self, *args, **kwargs) -> Any:
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
        self._executed_functions.append(func_info)
        if inspect.iscoroutinefunction(func_info.function_object):
            return await func_info.function_object(self._operation_self_obj, **args)
        else:
            return func_info.function_object(self._operation_self_obj, **args)


class OperationTransactionManager:
    def __init__(self, exception_handlers_mapping: Optional[dict[Type, Callable]] = None):
        self.exception_handlers_mapping = exception_handlers_mapping or {}

    def _get_handler_by_exception(self, exc: Exception) -> Optional[Callable]:
        for cls in inspect.getmro(exc.__class__):
            handler = self.exception_handlers_mapping.get(cls, None)
            if handler is not None:
                return handler

    def handle_exception(self, exc: Exception, op: Operation) -> Any:
        handler = self._get_handler_by_exception(exc)
        if handler is None:
            return exc
        else:
            return handler(exc, op)

    async def ahandle_exception(self, exc: Exception, op: Operation):
        handler = self._get_handler_by_exception(exc)
        if handler is None:
            return exc
        else:
            if inspect.iscoroutinefunction(handler):
                return await handler(exc, op)
            return handler(exc, op)
