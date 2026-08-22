install:
	docker compose up --build
run:
	docker compose up
stop:
	docker compose down
uninstall:
	docker compose down --rmi all -v