.PHONY: bootstrap build start stop status restart bash logs shell initdb migratedb upgradedb test lint

bootstrap: stop build start upgradedb

build:
	@docker-compose build --force-rm

start:
	@docker-compose up -d

stop:
	@docker-compose down

status:
	@docker-compose ps

restart: stop start

bash:
	@docker-compose run --rm flask-dev bash

logs:
	@docker-compose logs --follow 

shell:
	@docker-compose run --rm flask-dev flask shell

initdb:
	@docker-compose run --rm flask-dev flask db init

migratedb:
	@docker-compose run --rm flask-dev flask db migrate

upgradedb:
	@docker-compose run --rm flask-dev flask db upgrade

test:
	@docker-compose run --rm flask-dev flask test

lint:
	@docker-compose run --rm flask-dev flask lint