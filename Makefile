run:
	python solution.py
test:
	pytest . -sv
bench:
	python benchmark.py --ds-size=1000000
