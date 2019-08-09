test:
	docker-compose run --rm pytest

lint:
	docker-compose run --rm pylint