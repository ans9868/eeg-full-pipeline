# EEG Full Pipeline - Root Makefile
# This Makefile provides convenient commands for testing and development

# Test targets
test:
	@echo "🧪 Running all tests..."
	@echo "📊 Root repository tests..."
	python -m pytest tests/ -v --tb=short
	@echo "📊 PySpark pipeline tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite unit
	@echo "✅ All tests completed!"

test-root:
	@echo "🧪 Running root repository tests..."
	python -m pytest tests/ -v --tb=short

test-pyspark:
	@echo "🧪 Running PySpark pipeline tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite unit

test-pyspark-all:
	@echo "🧪 Running all PySpark pipeline tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite all

test-pyspark-integration:
	@echo "🧪 Running PySpark integration tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite integration

test-pyspark-transformers:
	@echo "🧪 Running PySpark transformer tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite transformers

test-pyspark-data-io:
	@echo "🧪 Running PySpark data I/O tests..."
	cd eeg-pyspark-pipeline && python run_tests.py --suite data_io

test-master:
	@echo "🧪 Running master test runner..."
	python run_all_tests.py --components pyspark root

test-master-verbose:
	@echo "🧪 Running master test runner (verbose)..."
	python run_all_tests.py --components pyspark root --verbose

test-master-coverage:
	@echo "🧪 Running master test runner with coverage..."
	python run_all_tests.py --components pyspark root --coverage

test-containerized:
	@echo "🧪 Running containerized tests..."
	cd eeg-pyspark-pipeline && ./run_tests_container.sh

# Pipeline execution targets
run:
	@echo "🚀 Running EEG pipeline with buildnrun.sh..."
	@if [ -z "$(CONFIG)" ]; then \
		echo "📋 Usage: make run CONFIG=\"<config_file> [options]\""; \
		echo "💡 Example: make run CONFIG=\"config/config_demo1.yaml\""; \
		echo "💡 Example: make run CONFIG=\"config/config_demo1.yaml --verbose\""; \
		exit 1; \
	fi
	@echo "🔧 Executing: ./buildnrun.sh $(CONFIG)"
	./buildnrun.sh $(CONFIG)

# Development targets
setup:
	@echo "🔧 Setting up development environment..."
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt
	@echo "✅ Development environment ready!"

# Utility targets
clean:
	@echo "🧹 Cleaning up..."
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name ".pytest_cache" -delete
	find . -type d -name ".coverage" -delete
	@echo "✅ Cleanup completed!"

help:
	@echo "🧪 EEG Full Pipeline - Available Commands:"
	@echo ""
	@echo "📊 Testing Commands:"
	@echo "  make test                    - Run all tests (root + PySpark unit)"
	@echo "  make test-root               - Run root repository tests only"
	@echo "  make test-pyspark            - Run PySpark unit tests only"
	@echo "  make test-pyspark-all        - Run all PySpark tests"
	@echo "  make test-pyspark-integration- Run PySpark integration tests"
	@echo "  make test-pyspark-transformers- Run PySpark transformer tests"
	@echo "  make test-pyspark-data-io    - Run PySpark data I/O tests"
	@echo "  make test-master             - Run master test runner"
	@echo "  make test-master-verbose     - Run master test runner (verbose)"
	@echo "  make test-master-coverage    - Run master test runner with coverage"
	@echo "  make test-containerized      - Run containerized tests"
	@echo ""
	@echo "🚀 Pipeline Execution Commands:"
	@echo "  make run CONFIG=\"<config>\"   - Run EEG pipeline with buildnrun.sh"
	@echo ""
	@echo "🔧 Development Commands:"
	@echo "  make setup                   - Set up development environment"
	@echo "  make clean                   - Clean up temporary files"
	@echo "  make help                    - Show this help message"
	@echo ""
	@echo "📁 Sub-repository Commands:"
	@echo "  cd eeg-pyspark-pipeline && make <target>  - PySpark pipeline commands"
	@echo "  cd eeg-ray-tuner && make <target>         - Ray tuner commands"

.PHONY: test test-root test-pyspark test-pyspark-all test-pyspark-integration test-pyspark-transformers test-pyspark-data-io test-master test-master-verbose test-master-coverage test-containerized run setup clean help
