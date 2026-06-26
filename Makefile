.PHONY: help test test-unit

help: ## Show available targets
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-18s %s\n", $$1, $$2}'

test: test-unit ## Run all tests

test-unit: ## Fast static validation of the plugin (frontmatter, structure, manifest integrity)
	python3 -m pytest tests/unit -q
