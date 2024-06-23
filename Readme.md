# getNoteAPI
> Connected with hackMD API, easy to deploy and quick to use.

## Update record
* 04/18/2024: Version one online
* 04/19/2024: Add cache
* 04/20/2024: 
  * Add Private tags, if notes have "Private" tag, it can't be get by client.
  * Add IMG tags, get_notesList router will return each tags name 、 counts and img.
* 05/26/2024: Add router path for healthy check.

### Setup
* [Get Your HackMD token](https://hackmd.io/@hackmd-api/developer-portal/https%3A%2F%2Fhackmd.io%2F%40hackmd-api%2FrkoVeBXkq)
* Please obtain your HackMD token first, and then create a .env file. Write your token in the file as shown in the example below:
```python
# .env
hackmd_token=<your_hackmd_token>
```

### 1. Run local
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
# healthy check
curl -X 'GET' \
  'http://localhost:8000/api/v1/ping' \
  -H 'accept: application/json'

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
# ping
{
  "result": "alive"
}

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
```python
JSONResponse({'result': 'NO_RESULT_ERROR'}, 400)
```
#### INTERNAL_ERROR
```python
JSONResponse({'result': 'INTERNAL_ERROR'}, 500)
```
