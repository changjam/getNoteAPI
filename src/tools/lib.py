import logging
from functools import wraps
from typing import Any, Callable, Coroutine, ParamSpec
from dataclasses import dataclass
from pydantic import BaseModel
from fastapi.responses import JSONResponse

LAST_SAVE_TIME: int = None

class NID(BaseModel):
    nid: str

class TAG(BaseModel):
    tag: str

class Note_Data(BaseModel):
    id: str
    title: str
    tags: str
    content: str
    lastUpdate: str

class Note_List_Data(BaseModel):
    notes_num: int
    tags_list: list
    notes_info: list[Note_Data]


@dataclass
class Errors:
    NOTES_NOT_EXIST_ERROR = JSONResponse({'result': 400}, 400)
    NO_RESULT_ERROR = JSONResponse({'result': 400}, 400)
    INTERNAL_ERROR = JSONResponse({'result':999}, 500)

P = ParamSpec('P')

def catch_error(func: Callable[P, Coroutine[Any, Any, Any]]) -> Callable[P, Coroutine[Any, Any, Any]]:
    @wraps(func)
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Any:
        try:
            return await func(*args, **kwargs)
        except Exception as ex:
            logging.getLogger('uvicorn.error').error(str(ex), exc_info=True, stack_info=True)
            return Errors.INTERNAL_ERROR

    return wrapper