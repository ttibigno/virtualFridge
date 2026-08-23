.PHONY: install run stop uninstall cleanup

install:
	docker compose up --build
run:
	docker compose up
stop:
	docker compose down
uninstall:
	docker compose down --remove-orphans --rmi all -v
cleanup:
	docker compose down --remove-orphans --rmi all -v
	docker system prune -af