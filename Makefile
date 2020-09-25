start:
	@docker-compose up -d database flask-dev

rebuild:
	@docker-compose up -d --build database flask-dev

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
	@docker-compose run --rm flask-dev pipenv run flask shell

initdb:
	@docker-compose run --rm flask-dev pipenv run flask db init

migratedb:
	@docker-compose run --rm flask-dev pipenv run flask db migrate

upgradedb:
	@docker-compose run --rm flask-dev pipenv run flask db upgrade

test:
	@docker-compose run --rm flask-dev pipenv run flask test

lint:
	@docker-compose run --rm flask-dev pipenv run flask lint