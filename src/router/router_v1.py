from fastapi import APIRouter
from fastapi.responses import JSONResponse
from tools.lib import *
from tools.method import (
                        isExpire,
                        update,
                        get_note_list_data,
                        write_note_list_data,
                        get_tags,
                        get_notes_data,
                        get_note_data,
                        write_note_data,
                        set_note_data,
                        check_notes_id_exist,
                        change_last_saveTime_format)

router = APIRouter(prefix="/api/v1", tags=['v1'])


@router.get("/get_notesList")
async def get_notesList():
    global LAST_SAVE_TIME
    note_list_data: list = get_note_list_data()
    write_note_list_data(note_list_data)

    if isExpire(LAST_SAVE_TIME, limit_time_minute = 1):
        note_list_data, LAST_SAVE_TIME = update(note_list_data)

    tags: list | None = get_tags(note_list_data)
    
    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))
    
    # check result
    if not tags or len(tags) == 0:
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=tags, status_code=200)

@router.post("/get_notes_by_tag")
@catch_error
async def get_notes_by_tag(tag_input: TAG):
    global LAST_SAVE_TIME
    tag: str = tag_input.tag

    if tag == 'Private':
        return Errors.NOTES_NOT_EXIST_ERROR

    note_list_data: list = get_note_list_data()
    write_note_list_data(note_list_data)

    if isExpire(LAST_SAVE_TIME, limit_time_minute = 1):
        note_list_data, LAST_SAVE_TIME = update(note_list_data)
    
    result: list = get_notes_data(note_list_data, tag)
    
    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))

    # check result
    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)

@router.post("/get_note_by_id")
@catch_error
async def get_note_by_id(nid_input: NID):
    global LAST_SAVE_TIME
    nid: str = nid_input.nid
    data_path: str = f'notes/{nid}.json'
    note_data: list = []

    # check is expire
    if isExpire(LAST_SAVE_TIME, limit_time_minute = 60*24):
        note_list_data: list = get_note_list_data()
        note_list_data, LAST_SAVE_TIME = update(note_list_data)

    # check nid exist
    if not check_notes_id_exist(nid):
        return Errors.NOTES_NOT_EXIST_ERROR

    # check path exist
    note_data = get_note_data(data_path, nid)
    write_note_data(data_path, note_data)
    result: Note_Data = set_note_data(note_data)

    print('last save time: ', change_last_saveTime_format(LAST_SAVE_TIME))

    # check result
    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)