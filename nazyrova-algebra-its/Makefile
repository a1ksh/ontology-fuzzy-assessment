.PHONY: setup test reproduce clean
setup:      ## install dependencies
	pip install -r requirements.txt
test:       ## run unit tests (reproduces the Table 4 example)
	python -m pytest -q tests/
reproduce:  ## reproduce all tables/figures into results/
	python experiments/run_all.py
clean:
	rm -rf results/*.csv results/*.png src/__pycache__ tests/__pycache__
