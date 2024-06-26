REGISTRY = "ghcr.io"

LOGIN = "tatiana-bosacheva"

IMAGE = "nfa_app"

IMAGE_REF := $(REGISTRY)/$(LOGIN)/$(IMAGE)


image_build:
	docker build --tag $(IMAGE_REF) .

format:
	black liq_rates.py
	isort liq_rates.py

lint:
	flake8 liq_rates.py

run_script:
	python 3.10 liq_rates.py
