REVISION_TEXT?= $(shell date)

revision:
	alembic revision --autogenerate -m "$(REVISION_TEXT)"

upgrade:
	alembic upgrade head

one_version_downgrade:
	alembic downgrade -1

test:
	pytest