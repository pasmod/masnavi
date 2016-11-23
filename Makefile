name = masnavi-ai

build: stop
	docker build -t $(name) .
	docker run -d --name=$(name) $(name)
	docker cp $(name):/piplib lib/

stop:
	docker rm -f $(name) || true

start: stop
	docker run -d -v $(shell pwd):/var/www \
		--name=$(name) $(name) bash python main.py

run: stop
	docker run -it --rm=true -v $(shell pwd):/var/www \
		--name=$(name) $(name) bash -l
push:
	gcloud build-it gcr.io/$(name)/masnavi

deploy:
	appcfg.py update -A $(name) -V v3 .
