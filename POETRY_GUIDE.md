# 🎯 Poetry Quick Reference Guide

Your project now uses Poetry for dependency management! This guide shows you how to use it.

## What Changed

### Before (with pip + requirements.txt):
```bash
source venv/bin/activate  # Activate virtual environment
pip install -r requirements.txt  # Install dependencies
python app.py  # Run app
```

### After (with Poetry):
```bash
poetry install  # Install all dependencies
poetry run python app.py  # Run app
# OR
poetry shell  # Enter Poetry's virtual environment
python app.py  # Then run commands directly
```

## Common Commands

### Installing Dependencies

```bash
# Install all dependencies from pyproject.toml
poetry install

# Install without dev dependencies (for production)
poetry install --without dev
```

### Adding New Packages

```bash
# Add a production dependency
poetry add flask-mail

# Add with specific version
poetry add flask-mail==0.9.1

# Add a development dependency (like pytest)
poetry add pytest --group dev
```

### Removing Packages

```bash
# Remove a package
poetry remove flask-mail
```

### Running Your App

```bash
# Option 1: Use poetry run
poetry run python app.py
poetry run pytest  # Run tests

# Option 2: Activate Poetry's shell
poetry shell  # Activates the virtual environment
python app.py  # Now run commands directly
exit  # When done, exit the shell
```

### Updating Dependencies

```bash
# Update all packages to latest compatible versions
poetry update

# Update a specific package
poetry update flask

# Show what would be updated (dry run)
poetry update --dry-run
```

### Viewing Installed Packages

```bash
# List all installed packages
poetry show

# Show dependency tree
poetry show --tree

# Show info about a specific package
poetry show flask
```

## Understanding Your Files

### pyproject.toml
This is your project configuration file. It's like an enhanced `requirements.txt`:

```toml
[project]
name = "personal-finance-app"
version = "0.1.0"
description = "A personal finance tracking application for learning"

dependencies = [
    "flask (==3.0.0)",
    "flask-sqlalchemy (==3.1.1)",
    # ... more packages
]

[dependency-groups]
dev = [
    "pytest (==8.0.0)"
]
```

**You can edit this file directly!** Poetry will pick up changes when you run `poetry install`.

### poetry.lock
This file contains exact versions of ALL packages (including sub-dependencies). 

**Don't edit this manually!** Poetry manages it automatically.

**Do commit it to Git!** This ensures everyone gets the same versions.

## Your Startup Script

Your `start.sh` now uses Poetry:

```bash
./start.sh  # Works as before!
```

It now runs `poetry run python app.py` instead of activating venv manually.

## Comparing to Old Workflow

| Task | Old Way (pip) | New Way (Poetry) |
|------|---------------|------------------|
| Install dependencies | `pip install -r requirements.txt` | `poetry install` |
| Add package | `pip install flask-mail` then manually update requirements.txt | `poetry add flask-mail` |
| Remove package | `pip uninstall flask-mail` then manually update requirements.txt | `poetry remove flask-mail` |
| Run app | `source venv/bin/activate && python app.py` | `poetry run python app.py` |
| Run tests | `source venv/bin/activate && pytest` | `poetry run pytest` |

## Benefits You Get

### 1. Automatic Conflict Resolution
**Before:** If you installed a package that needed a different SQLAlchemy version, pip might break your app.

**Now:** Poetry checks all dependencies and prevents conflicts before installing.

### 2. Reproducible Installs
**Before:** `requirements.txt` had your packages but not the sub-dependencies.

**Now:** `poetry.lock` locks EVERY package to exact versions, so anyone can reproduce your exact environment.

### 3. Simpler Package Management
**Before:** Install package → Manually add to requirements.txt → Remember the version

**Now:** `poetry add package` does everything automatically.

### 4. Separate Dev Dependencies
**Before:** Mix of production and development packages in requirements.txt

**Now:** Dev tools (like pytest) are separate and won't be installed in production.

## Real-World Example

Let's say you want to add email support:

### Old Way:
```bash
source venv/bin/activate
pip install flask-mail
# Oh no, what version did it install?
pip freeze | grep flask-mail  # Check the version
# Manually edit requirements.txt and add: flask-mail==0.10.0
```

### Poetry Way:
```bash
poetry add flask-mail
# Done! Poetry:
# - Resolved all dependencies
# - Updated pyproject.toml
# - Updated poetry.lock
# - Installed the package
```

## Tips & Tricks

### Tip 1: Poetry Shell vs Poetry Run

```bash
# If you're running many commands:
poetry shell
python app.py
pytest
python seed_data.py
exit

# If you're running one command:
poetry run python app.py
```

### Tip 2: Check What Changed

```bash
# See what poetry show will install/update
poetry show --outdated
```

### Tip 3: Clean Start

```bash
# Remove poetry's virtual environment and start fresh
poetry env remove python
poetry install
```

### Tip 4: VS Code / Cursor Integration

Poetry creates its virtual environment in a different location. To use it in your IDE:

```bash
# Find where Poetry's virtual environment is:
poetry env info --path

# Copy that path and set it as your Python interpreter in VS Code/Cursor
```

## Troubleshooting

### "Command not found: poetry"

Poetry is installed via Homebrew. Make sure Homebrew's bin is in your PATH:
```bash
echo 'export PATH="/opt/homebrew/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### "This project seems to be broken"

Try recreating the environment:
```bash
poetry env remove python
poetry install
```

### "Python version not compatible"

Check your Python version:
```bash
python3 --version
```

Update `pyproject.toml` if needed:
```toml
requires-python = "^3.9"  # Adjust to your Python version
```

## Next Steps

1. ✅ Poetry is installed and working
2. ✅ Your dependencies are managed by Poetry
3. ✅ Your startup script uses Poetry
4. ✅ You can still run `./start.sh` as before

**You're all set!** Your old `venv` folder is still there but not used anymore. You can delete it if you want:

```bash
rm -rf venv
```

## Learn More

- [Poetry Documentation](https://python-poetry.org/docs/)
- [Managing Dependencies](https://python-poetry.org/docs/managing-dependencies/)
- [Commands Reference](https://python-poetry.org/docs/cli/)

---

**Questions?** Just ask! Poetry makes Python dependency management much easier once you get used to it.
