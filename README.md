# FastAPI implementation

This repository is the response to a coding challenge from BreakthroughEnergy, implemented in stages according to the instructions.

## Usage

To use this repository it is recommended to first create a python virtual environment via the following commands

```
# Create virtual environment
python -m venv venv

# Activate the virtual environment

# Windows
venv\Scripts\activate

# Unix/MacOS
source venv/bin/activate
```

Regardless of whether you utilize a virtual environment install the required dependencies for this project via `pip install -r requirements.txt`

Once the requirements are installed the API backend of this project can be initialized by the command `make run` which will start the project at `http://localhost:8000`

## Testing

This repository includes tests, you can run them via `make test`

## Endpoints 

GET `/helloworld`: returns a "Hellow World!" message

- Set `Accept: application/json` header for a JSON response
- Add `tz` parameter with IANA timezone to customize message with timezone information

POST `/unravel`: restructures valid JSON into a list of elements

- Body can be any valid JSON

POST `/roll`: pulls and updates the repository

### Example 1

```bash
curl --location 'localhost:8000/unravel' \
--header 'Content-Type: application/json' \
--data '{
    "test 1": [
        1,
        2,
        3
    ],
    "test 2": "result",
    "test 3": {
        "subtest 1": 1,
        "subtest 2": [
            1,
            2,
            3
        ],
        "subtest 3": "result"
    }
}'
```
### Response 

`["test 1",1,2,3,"test 2","result","test 3","subtest 1",1,"subtest 2",1,2,3,"subtest 3","result"]`

### Example 2
```bash
curl --location 'localhost:8000/unravel' \
--header 'Content-Type: application/json' \
--data '"test"'
```

### Response
`["test"]`

### Example 3
```bash
curl --location 'localhost:8000/unravel' \
--header 'Content-Type: application/json' \
--data '[1,2,3]'
```

### Response
`[1,2,3]`

Test Update