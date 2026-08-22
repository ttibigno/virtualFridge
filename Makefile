install:
	docker compose up --build
run:
	docker compuse up
stop:
	docker compose down
uninstall:
	docker compose down --rmi all