# HyStats Private API
Private API used for internal tools to grab statistics/data from the database
## Installation
- Install dependencies (Python 3+ and pip need to be installed)
```
pip install fastapi
pip install uvicorn
pip install mysql-connector-python
```
- Pull files from this repo and fill out `config.py`.
## How to run
```
uvicorn main:app --host 0.0.0.0 --port 80
```
