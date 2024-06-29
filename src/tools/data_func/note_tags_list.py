import json
from collections import defaultdict

from tools.data_func import isPrivate
from tools.data_func.note import get_note_data




def get_tags_obj_list(data: list) -> list | None:
    def zero():
        return 0
    try:
        result = defaultdict(zero)
        img_obj: dict = {}
        for note in data:
            if isPrivate(note['tags']):
                if 'IMG' in note['tags']:
                    nid = note['id']
                    img_info = get_note_data(f'notes/{nid}.json', nid)
                    img_obj = json.loads(img_info['content'])
            elif note['tags']:
                tag = note['tags'][0]
                result[tag] += 1

        return [{"category": key, "counts": value, "img": img_obj.get(key, "")} for key, value in result.items()]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
