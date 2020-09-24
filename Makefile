start:
	@docker-compose up -d database flask-dev

stop:
	@docker-compose down

status:
	@docker-compose ps

restart: stop start

shell:
	@docker-compose run --rm manage shell

logs:
	@docker-compose logs --follow 

initdb:
	@docker-compose run --rm manage db init

migratedb:
	@docker-compose run --rm manage db migrate

upgradedb:
	@docker-compose run --rm manage db upgrade

test:
	@docker-compose run --rm manage test

lint:
	@docker-compose run --rm manage lint