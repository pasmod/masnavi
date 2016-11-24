name = masnavi

build: stop
	docker build -t $(name) .

stop:
	docker rm -f $(name) || true

start: stop
	docker run -d -p 5000:5000 -v $(shell pwd):/var/www \
		--name=$(name) $(name) python main.py

run: stop
	docker run -it --rm=true -v $(shell pwd):/var/www \
		--name=$(name) $(name) bash -l
