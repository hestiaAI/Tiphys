# Tiphys
Tiphys – Pilot of [Argonodes](https://github.com/hestiaAI/Argonodes) – Model creation wizard

## Setup
1. `cd /path/to/project`
2. `python -m venv ./env`
3. `source ./env/bin/activate`
4. `pip install -r requirements.txt`
5. TODO script to install pyscript
6. `pre-commit install`
7. `cp secret.py.dist secret.py`
8. Change values inside the `secret.py` file by random key and default user password.
9. `python init_db.py`

## Usage
1. `python app.py`
2. Open http://127.0.0.1:5000/ in browser

## Deployment
[Read here](https://flask.palletsprojects.com/en/2.0.x/deploying/).
