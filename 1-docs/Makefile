# Blackbox5 Documentation Makefile

.PHONY: index check watch install-hooks clean

# Generate the documentation index
index:
	@echo "📚 Generating documentation index..."
	@python3 ../bin/generate-docs-index.py

# Check if index is current (for CI)
check:
	@echo "🔍 Checking if INDEX.md is current..."
	@python3 ../bin/generate-docs-index.py --check

# Watch for changes and auto-regenerate
watch:
	@echo "👁️  Watching for changes (Ctrl+C to stop)..."
	@python3 ../bin/generate-docs-index.py --watch

# Install git hooks for auto-generation
install-hooks:
	@echo "🔧 Installing git hooks..."
	@../bin/install-docs-hooks.sh

# Clean generated files
clean:
	@echo "🧹 Cleaning generated files..."
	@rm -f INDEX.md

# Show help
help:
	@echo "Blackbox5 Documentation Commands:"
	@echo ""
	@echo "  make index         - Generate INDEX.md from current structure"
	@echo "  make check         - Verify INDEX.md is current (CI mode)"
	@echo "  make watch         - Watch for changes and auto-regenerate"
	@echo "  make install-hooks - Install git hooks for auto-generation"
	@echo "  make clean         - Remove generated INDEX.md"
	@echo "  make help          - Show this help"
