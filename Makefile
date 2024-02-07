docker-build-dev:
	docker build --tag=dev --target=dev .

docker-build-tests:
	docker build --tag=tests --target=tests .

docker-run-tests: docker-build-tests
	docker run --rm -it tests

docker-run-dev-sh: docker-build-dev
	docker run --rm -it --entrypoint sh dev
