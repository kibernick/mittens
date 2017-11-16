console:
	FLASK_APP=autoapp.py FLASK_DEBUG=1 flask shell

app:
	FLASK_APP=autoapp.py FLASK_DEBUG=1 flask run

pipup:
	pip-compile; pip install -r requirements.txt

test:
	PYTHONPATH=. pytest tests

localdb:
	PYTHONPATH=. python scripts/init_local_db.py
