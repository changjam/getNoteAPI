from tools.data_func import isPrivate, set_note_data




def get_notes_data(data: list, tag: str) -> list:
    title_list: list = []
    for note in data:
        if note['tags']:
            if tag in note['tags'] and not isPrivate(note['tags']):
                note_data = set_note_data(note)
                del note_data['content']
                title_list.append(note_data)
    return title_list