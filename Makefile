test:
	pipenv run black --check src/
	pipenv run python src/manage.py test apps

init:
	pipenv update --dev
