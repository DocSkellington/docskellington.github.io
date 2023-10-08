build:
	pipenv run python main.py

dependencies:
	pipenv --python 3.11
	pipenv install --dev

clean:
	rm -fr output

nuke: clean
	pipenv --rm
	rm -f Pipfile.lock
