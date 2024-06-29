from fastapi import APIRouter
from fastapi.responses import JSONResponse

from tools.lib import *
from tools.data_func import (
                                HACKMD_API,
                                isExpire, 
                                change_last_saveTime_format, 
                                get_note_list_data, 
                                write_note_list_data, 
                                update_note_list_data, 
                                set_note_data
                            )
from tools.data_func.note_tags_list import get_tags_obj_list
from tools.data_func.notes_data import get_notes_data
from tools.data_func.note import (
                                    check_notes_id_exist, 
                                    get_note_data, 
                                    write_note_data
                                )




router = APIRouter(prefix="/api/v1", tags=['v1'])

@router.get("/ping")
def ping():
    return JSONResponse(content={"result": "alive"}, status_code=200)


@router.get("/get_tags_list")
@router_catch_error
async def get_tags_list():
    global LAST_SAVE_TIME
    if not HACKMD_API or HACKMD_API == '':
        return Errors.NO_TOKEN_ERROR

    # 1. get note list data
    note_list_data: list = get_note_list_data()
    write_note_list_data(note_list_data)

    if isExpire(LAST_SAVE_TIME, limit_time_minute = 1):
        note_list_data, LAST_SAVE_TIME = update_note_list_data(note_list_data)

    # 2. get tags obj list
    tags_obj_list: list | None = get_tags_obj_list(note_list_data)
    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))
    
    if not tags_obj_list or len(tags_obj_list) == 0:
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=tags_obj_list, status_code=200)


@router.post("/get_notes_by_tag")
@router_catch_error
async def get_notes_by_tag(tag_input: TAG):
    global LAST_SAVE_TIME
    if not HACKMD_API or HACKMD_API == '':
        return Errors.NO_TOKEN_ERROR
    
    tag: str = tag_input.tag

    if tag == 'Private':
        return Errors.NOTES_NOT_EXIST_ERROR

    # 1. get note list data
    note_list_data: list = get_note_list_data()
    write_note_list_data(note_list_data)

    if isExpire(LAST_SAVE_TIME, limit_time_minute = 1):
        note_list_data, LAST_SAVE_TIME = update_note_list_data(note_list_data)
    
    # 2. get notes data by tag
    result: list = get_notes_data(note_list_data, tag)
    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))

    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)


@router.post("/get_note_by_id")
@router_catch_error
async def get_note_by_id(nid_input: NID):
    global LAST_SAVE_TIME
    if not HACKMD_API or HACKMD_API == '':
        return Errors.NO_TOKEN_ERROR
    
    nid: str = nid_input.nid
    data_path: str = f'notes/{nid}.json'
    note_data: list = []

    # 1. get note list data
    note_list_data: list = get_note_list_data()

    if isExpire(LAST_SAVE_TIME, limit_time_minute = 60*24):
        note_list_data, LAST_SAVE_TIME = update_note_list_data(note_list_data)

    if not check_notes_id_exist(nid, note_list_data):
        return Errors.NOTES_NOT_EXIST_ERROR

    # 2. get note data by id
    note_data = get_note_data(data_path, nid)
    write_note_data(data_path, note_data)
    result: Note_Data = set_note_data(note_data)

    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))

    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)