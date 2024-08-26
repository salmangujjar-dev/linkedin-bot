run:
	uvicorn main:app --reload

install:
	pip install -r requirements.txt

lint:
	flake8 .