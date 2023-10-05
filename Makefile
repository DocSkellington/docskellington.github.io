build:
	pipenv run python main.py

dependencies:
	mkdir .venv
	pipenv install --dev

clean:
	rm -r output
	rm -fr .venv
	rm Pipfile.lock
