#!/bin/bash
# Script to run tests for Harit Finance app
# Archived: Use `poetry run pytest tests/ -v` instead (see README.md)

echo "🧪 Running Harit Finance Test Suite..."
echo "======================================"
echo ""

# Run all tests with verbose output
pytest tests/ -v --tb=short

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ All tests passed!"
    echo ""
    echo "Want more details? Try:"
    echo "  pytest tests/ -v           # Verbose output"
    echo "  pytest tests/ --cov=.      # With coverage"
    echo "  pytest tests/ -k transfer  # Run only transfer tests"
else
    echo ""
    echo "❌ Some tests failed. Check the output above."
fi
