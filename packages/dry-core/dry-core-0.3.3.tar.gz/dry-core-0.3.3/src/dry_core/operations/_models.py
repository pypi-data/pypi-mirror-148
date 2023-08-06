from typing import Any, Type, Optional, Callable
from pydantic import BaseModel


class FunctionArgInfo(BaseModel):
    name: str
    type: Optional[Type] = None
    default_value: Optional[Any] = None


class FunctionInformation(BaseModel):
    function_object: Callable
    priority: int = -1
    args: dict[str, FunctionArgInfo] = {}

    @property
    def name(self) -> str:
        return self.function_object.__name__

    @property
    def receives_all_kwargs(self) -> bool:
        return "kwargs" in self.args.keys()
