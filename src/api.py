import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
from tools.lib import *
from tools.method import (
                        HACKMD_API,
                        isExpire,
                        update,
                        get_local_note_list_data,
                        get_tags,
                        get_title,
                        get_local_note_data,
                        write_local_note_data,
                        set_note_data)

app = FastAPI()

# 設定 CORS 標頭
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允許的前端網域
    allow_credentials=True,
    allow_methods=["*"],  # 允許的 HTTP 方法
    allow_headers=["*"],  # 允許的 HTTP 標頭
)



@app.post("/get_notesList")
async def get_notesList():
    global LAST_SAVE_TIME
    note_list_data: list = get_local_note_list_data()
    
    # if isExpire(LAST_SAVE_TIME, limit_time_minute = 10):
    #     note_list_data, LAST_SAVE_TIME = update(note_list_data)

    tags: list = get_tags(note_list_data)
    
    if len(tags) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=tags, status_code=200)

@app.post("/get_notes_by_tag")
@catch_error
async def get_notes_by_tag(tag_input: TAG):
    global LAST_SAVE_TIME
    tag: str = tag_input.tag
    note_list_data: list = get_local_note_list_data()

    # if isExpire(LAST_SAVE_TIME, limit_time_minute = 10):
    #     note_list_data, LAST_SAVE_TIME = update(note_list_data)
    
    result: list = get_title(note_list_data, tag)

    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)

@app.post("/get_note_by_id")
@catch_error
async def get_note_by_id(nid_input: NID) -> Note_Data:
    global LAST_SAVE_TIME
    nid: str = nid_input.nid
    data_path: str = f'notes/{nid}.json'
    note_data: list = []

    # if isExpire(LAST_SAVE_TIME, limit_time_minute = 60*24):
    #     note_list_data, LAST_SAVE_TIME = update(note_list_data)

    if os.path.exists(data_path):
        note_data = get_local_note_data(data_path)
    else:
        note_data = HACKMD_API.get_note(nid)
        write_local_note_data(data_path ,note_data)
    
    result: Note_Data = set_note_data(note_data)

    if len(result) == 0: 
        return Errors.NO_RESULT_ERROR

    return JSONResponse(content=result, status_code=200)




if __name__ == "__main__":
    uvicorn.run(app, host='0.0.0.0', port=8000, workers=1)
