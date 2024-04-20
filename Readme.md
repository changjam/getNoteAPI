# getNoteAPI
> 使用 hackMD API ， 簡單部屬，快速使用。

## 版本紀錄
* 04/18/2024: Version one online
* 04/20/2024: Add cache

### Setup 
### 1. 本地運行
```bash
pip install -r requirements.txt
cd src/
python api.py
```
### 2. Docker
```bash
docker build -t get_note_api .
docker run -p 8000:8000 -e hackmd_token=<your_hackmd_token> get_note_api
```

### Request
#### CURL
```bash
# get_notesList
curl -X 'GET' \
  'http://localhost:8000/api/v1/get_notesList' \
  -H 'accept: application/json'

# get_notes_by_tag
curl -X 'POST' \
  'http://localhost:8000/api/v1/get_notes_by_tag' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "tag": <note_tag>
}'

# get_note_by_id
curl -X 'POST' \
  'http://localhost:8000/api/v1/get_note_by_id' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "nid": <note_id>
}'
```

### Response
```python
# get_notesList
[
  {
    "category": "string",
    "counts": int
  }
]

# get_notes_by_tag
[
  {
    "id": "string",
    "title": "string",
    "tags": "string",
    "content": "",
    "lastUpdate": "string"
  }
]

# get_note_by_id
{
  "id": "string",
  "title": "string",
  "tags": "string",
  "content": "string",
  "lastUpdate": "string"
}
```
### Errors Response

#### NOTES_NOT_EXIST_ERROR
```python
JSONResponse({'result': 'NOTES_NOT_EXIST_ERROR'}, 400)
```
#### NO_RESULT_ERROR
```bash
JSONResponse({'result': 'NO_RESULT_ERROR'}, 400)
```
#### INTERNAL_ERROR
```bash
JSONResponse({'result': 'INTERNAL_ERROR'}, 500)
```
