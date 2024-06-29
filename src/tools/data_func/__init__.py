import os
import time
import json
import pytz
from datetime import datetime
from dotenv import load_dotenv
from PyHackMD import API

from tools.lib import Note_Data



load_dotenv()

hackmd_token = os.environ.get('hackmd_token', '')
HACKMD_API = API(hackmd_token)


def get_note_list_data() -> list:
    try:
        local_path: str = 'db/note_list_data.json'
        if not os.path.exists(local_path):
            return HACKMD_API.get_note_list()
        with open(local_path, 'r', encoding='utf-8') as note_list_data:
            return json.load(note_list_data)
    except Exception as e:
        print(f"An error occurred: {e}")
        return []

def write_note_list_data(new_data: list) -> None:
    with open('db/note_list_data.json', 'w', encoding='utf-8') as note_list_data:
        json.dump(new_data, note_list_data)

def update_note_list_data(note_list_data: list) -> tuple[list, float]:
    new_note_list_data: list = HACKMD_API.get_note_list()
    remove_diff_notes(new_note_list_data, note_list_data)
    write_note_list_data(new_note_list_data)
    current_timestamp = time.time()
    return new_note_list_data, current_timestamp

def isPrivate(tags: list) -> bool:
    return 'Private' in tags

def isExpire(last_save_time: float, limit_time_minute: int) -> bool:
    if not last_save_time:
        return True
    limit_time_seconds = limit_time_minute * 60
    current_timestamp: float = time.time()
    return (current_timestamp - last_save_time) > limit_time_seconds

def change_last_saveTime_format(last_save_time: int) -> str:
    dt_object = datetime.fromtimestamp(last_save_time)
    tz = pytz.timezone('Asia/Taipei')
    dt_object = dt_object.replace(tzinfo=pytz.utc).astimezone(tz)
    return dt_object.strftime('%Y-%m-%d %H:%M:%S')

def set_note_data(data: dict) -> Note_Data:
    dt_object = datetime.fromtimestamp(data['lastChangedAt'] / 1000)
    yyyymmdd_date = dt_object.strftime('%Y-%m-%d')

    note_data: Note_Data = {}
    note_data['id'] =  data['id']
    note_data['title'] = data['title']
    note_data['tags'] = data['tags'][0]
    note_data['content'] = data['content']
    note_data['lastUpdate'] = str(yyyymmdd_date)
    return note_data

def remove_diff_notes(new_data: list, old_data: list) -> None:
    old_data_dict: dict = {item["id"]: item for item in old_data}
    new_data_dict: dict = {item["id"]: item for item in new_data}

    for old_id, old_item in old_data_dict.items():
        new_item = new_data_dict.get(old_id)
        if new_item is None or old_item != new_item:
            remove_local_note_data(f'notes/{old_id}.json')

def remove_local_note_data(data_path: str) -> None:
    if os.path.exists(data_path):
        os.remove(data_path)