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
