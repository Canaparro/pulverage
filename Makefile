sa:
	mypy ./pulverage --strict
	autoflake --in-place --remove-unused-variables --remove-all-unused-imports -r .
	isort .
	black .
	flake8 --max-line-length=88 .
	pylint ./pulverage
