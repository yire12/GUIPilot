.PHONY: help install test lint format clean build check

help:
	@echo "Available commands:"
	@echo "  make install    - Install package in development mode"
	@echo "  make test       - Run tests"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make check      - Run all checks"
	@echo "  make build      - Build package"
	@echo "  make clean      - Clean build artifacts"

install:
	pip install -e .

test:
	pytest tests/ -v

lint:
	flake8 guipilot/ experiments/
	pylint guipilot/
	mypy guipilot/ --ignore-missing-imports || true

format:
	black guipilot/ experiments/
	isort guipilot/ experiments/

check: lint test

build:
	python -m build

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -type d -name __pycache__ -exec rm -r {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

check-rq1:
	cd experiments/rq1_screen_inconsistency && python check_requirements.py

check-rq2:
	cd experiments/rq2_flow_inconsistency && python check_requirements.py

check-rq4:
	cd experiments/rq4_case_study && python check_requirements.py

check-all-experiments: check-rq1 check-rq2 check-rq4

