.PHONY: test-hupsel
test-hupsel: ## Install the poetry environment and install the pre-commit hooks
	@echo "Testing Hupselbrook example"
	@poetry run pytest tests/test_cases.py::test_hupselbrook_model

.PHONY: test-grass
test-grass: ## Install the poetry environment and install the pre-commit hooks
	@echo "Running grass growth example"
	@poetry run pytest tests/test_cases.py::test_grassgrowth

.PHONY: test-meteo
test-meteo: ## Test the retrieval and conversion of meteodata
	@ echo "Running meteo tester"
	@poetry run pytest tests/test_meteo.py

.PHONY: test-soilprofile
test-soilprofile: ## Test the retrieval and conversion of soilprofile data
	@ echo "Running soilprofile tester"
	@poetry run pytest tests/test_bofeksoilprofile.py

.PHONY: test-simple
test-simple: ## Test the retrieval and converstion of meteodata
	@ echo "Running simple model tester"
	@poetry run pytest tests/test_cases.py::test_simple_model

.PHONY:test-table
test-table: ## Test the update of table data
	@ echo "Running table tester"
	@poetry run pytest tests/test_basemodel.py::test_table_update

.PHONY: testcheck
testcheck: ## Run code quality tools in test configuration
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a 2>&1 | tee .logs/log_ruff_raw.md
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy pyswap --config-file mypy.dev.ini 2>&1 | tee .logs/log_mypy_raw.md
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry . 2>&1 | tee .logs/log_deptry_raw.md

.PHONY: check
check: ## Run code quality tools.
	@echo "🚀 Checking Poetry lock file consistency with 'pyproject.toml': Running poetry check --lock"
	@poetry check --lock
	@echo "🚀 Linting code: Running pre-commit"
	@poetry run pre-commit run -a
	@echo "🚀 Static type checking: Running mypy"
	@poetry run mypy
	@echo "🚀 Checking for obsolete dependencies: Running deptry"
	@poetry run deptry .

.PHONY: test
test: ## Test the code with pytest
	@echo "🚀 Testing code: Running pytest"
	@poetry run pytest --cov --cov-config=pyproject.toml --cov-report=xml

.PHONY: build
build: clean-build ## Build wheel file using poetry
	@echo "🚀 Creating wheel file"
	@poetry build

.PHONY: clean-build
clean-build: ## clean build artifacts
	@rm -rf dist

.PHONY: publish
publish: ## publish a release to pypi.
	@echo "🚀 Publishing: Dry run."
	@poetry config pypi-token.pypi $(PYPI_TOKEN)
	@poetry publish --dry-run
	@echo "🚀 Publishing."
	@poetry publish

.PHONY: build-and-publish
build-and-publish: build publish ## Build and publish.

.PHONY: docs-test
docs-test: ## Test if documentation can be built without warnings or errors
	@poetry run mkdocs build -s

.PHONY: docs
docs: ## Build and serve the documentation
	@poetry run mkdocs serve

.PHONY: help
help:
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

.DEFAULT_GOAL := help
