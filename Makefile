.PHONY: install run test populate stress stop uninstall cleanup

install:
	./scripts/setup.sh
	docker compose up --build -d
run:
	docker compose up -d
test:
	docker compose -f compose.test.yaml up --build --abort-on-container-exit --exit-code-from tests
	docker compose -f compose.test.yaml down
populate:
	docker compose --profile tools run --rm scripts mockscanner.py $(N)
stress:
	docker compose --profile tools run --rm scripts stresstest.py $(N) $(ERROR)
stop:
	docker compose down
uninstall:
	docker compose down --remove-orphans --rmi all -v
cleanup:
	docker compose down --remove-orphans --rmi all -v
	docker system prune -af