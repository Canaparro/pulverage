sa:
	poetry run mypy ./pulverage --strict
	poetry run autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
	poetry run isort .
	poetry run black .
	poetry run flake8 --max-line-length=88 --radon-max-cc=10 .
	poetry run pylint ./pulverage

ut:
	poetry run pytest tests/