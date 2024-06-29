import os
import json

from tools.data_func import HACKMD_API, isPrivate




def get_note_data(data_path: str, nid: str) -> dict:
    if not os.path.exists(data_path):
        return HACKMD_API.get_note(nid)
    with open(data_path, 'r', encoding='utf-8') as note_data:
        return json.load(note_data)

def write_note_data(data_path: str, new_data: list) -> None:
    with open(data_path, 'w', encoding='utf-8') as note_data:
        json.dump(new_data, note_data)

def get_notes_id_list(data: list) -> set:
    id_list = []
    for note in data:
        if note['tags'] and not isPrivate(note['tags']): id_list.append(note['id'])
    return set(id_list)

def check_notes_id_exist(note_id: str, note_list_data: list) -> bool:
    note_id_list = get_notes_id_list(note_list_data)
    return note_id in note_id_list