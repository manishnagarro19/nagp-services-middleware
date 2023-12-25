.PHONY: install
install:
	@bash bin/install.sh

.PHONY: lint
lint:
	pre-commit run --all-files

.PHONY: one-time
one-time:
	pre-commit install

.PHONY: setup-rabbit-mq
setup-rabbit-mq:
	docker-compose -f rabbit_mq_setup/docker-compose.yml up
