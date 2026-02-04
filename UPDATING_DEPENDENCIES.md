# 📦 Updating Dependencies with Poetry

## Current Setup

Your `pyproject.toml` currently uses **exact version pinning**:

```toml
dependencies = [
    "flask (==3.0.0)",      # Exactly version 3.0.0
    "werkzeug (==3.0.1)",   # Exactly version 3.0.1
]
```

This is very safe but doesn't allow automatic updates.

## Version Constraint Strategies

### 1. Exact Pinning (What You Have Now) 🔒

```toml
"flask (==3.0.0)"
```

**Meaning:** Only use Flask 3.0.0, nothing else

**Pros:**
- ✅ Maximum stability
- ✅ No surprises
- ✅ Perfect reproducibility

**Cons:**
- ❌ Need to manually update each package
- ❌ Miss bug fixes and security patches

**Use when:** You want absolute control

### 2. Caret Constraint (^) - Recommended 🎯

```toml
"flask (^3.0.0)"
```

**Meaning:** >=3.0.0 but <4.0.0

**What gets updated:**
- ✅ 3.0.0 → 3.0.1 (patch)
- ✅ 3.0.0 → 3.1.0 (minor)
- ❌ 3.0.0 → 4.0.0 (major - blocked)

**Pros:**
- ✅ Get bug fixes automatically
- ✅ Get new features (minor updates)
- ✅ Won't break on major changes
- ✅ Balanced approach

**Cons:**
- ⚠️ Minor updates could theoretically introduce bugs

**Use when:** Normal development (most common)

### 3. Tilde Constraint (~) - Conservative

```toml
"flask (~3.0.0)"
```

**Meaning:** >=3.0.0 but <3.1.0

**What gets updated:**
- ✅ 3.0.0 → 3.0.5 (patch only)
- ❌ 3.0.0 → 3.1.0 (minor - blocked)
- ❌ 3.0.0 → 4.0.0 (major - blocked)

**Pros:**
- ✅ Only get bug fixes
- ✅ Very safe

**Cons:**
- ❌ Miss new features

**Use when:** You want stability but some updates

### 4. Greater Than (>=) - Flexible

```toml
"flask (>=3.0.0)"
```

**Meaning:** 3.0.0 or any newer version

**Pros:**
- ✅ Always get latest

**Cons:**
- ⚠️ Can break on major updates

**Use when:** You want bleeding edge (not recommended)

## Recommended Strategy

For your learning project, I recommend **caret constraints (^)**:

```toml
dependencies = [
    "flask (^3.0.0)",           # Get 3.x updates, not 4.x
    "flask-sqlalchemy (^3.1.1)",
    "flask-login (^0.6.3)",
    "sqlalchemy (^2.0.23)",
    "werkzeug (^3.0.1)",
]
```

This way:
- `poetry update` gets you bug fixes and new features
- Major breaking changes are blocked
- Best balance of safety and freshness

## How to Update

### Step-by-Step Update Process

#### 1. Check What's Available

```bash
# See what updates are available
poetry show --outdated
```

Example output:
```
flask         3.0.0  →  3.1.0  
werkzeug      3.0.1  →  3.1.5  
pytest        8.0.0  →  8.4.2  
```

#### 2. Test Update (Dry Run)

```bash
# See what WOULD change without actually changing it
poetry update --dry-run
```

Output shows:
```
Package operations: 0 installs, 3 updates, 0 removals

  - Updating flask (3.0.0 -> 3.1.0)
  - Updating werkzeug (3.0.1 -> 3.1.5)
  - Updating pytest (8.0.0 -> 8.4.2)
```

#### 3. Update Specific Package

```bash
# Update just Flask (safest)
poetry update flask

# Test your app
poetry run python app.py
poetry run pytest
```

#### 4. Update Everything

```bash
# Update all packages at once
poetry update

# Test thoroughly
poetry run pytest
poetry run python app.py
```

### Real Example

Let's say Flask 3.1.0 is released with bug fixes:

```bash
# 1. Check what's new
poetry show --outdated

# 2. See what would change
poetry update flask --dry-run

# 3. Update Flask
poetry update flask

# Output:
# Updating dependencies
# Resolving dependencies...
# 
# Package operations: 0 installs, 1 update, 0 removals
# 
#   - Updating flask (3.0.0 -> 3.1.0)
# 
# Writing lock file

# 4. Test your app
poetry run python app.py
# ✅ Works!
```

## Updating Specific Versions

### Upgrade to Specific Version

```bash
# Want Flask 3.1.0 specifically?
poetry add flask@3.1.0

# Or use add with ==
poetry add "flask==3.1.0"
```

### Upgrade to Latest

```bash
# Get the latest version available
poetry add flask@latest
```

## Changing Your Version Strategy

Want to switch from exact (`==`) to caret (`^`) constraints?

### Option 1: Edit pyproject.toml Directly

Open `pyproject.toml` and change:

```toml
# From:
dependencies = [
    "flask (==3.0.0)",
]

# To:
dependencies = [
    "flask (^3.0.0)",
]
```

Then run:
```bash
poetry lock --no-update  # Update lock file only
poetry install           # Install with new constraints
```

### Option 2: Re-add Packages

```bash
# Remove and re-add with caret
poetry remove flask
poetry add "flask^3.0.0"
```

## Best Practices

### 1. Update Regularly (But Not Too Often)

```bash
# Good schedule:
# - Check monthly: poetry show --outdated
# - Update quarterly: poetry update
# - Update immediately for security fixes
```

### 2. Update One at a Time for Major Changes

```bash
# If updating major version (e.g., 2.x → 3.x):
poetry add flask@^3.0  # Just Flask first
poetry run pytest      # Test everything
# If good, continue with others
```

### 3. Always Test After Updating

```bash
poetry update
poetry run pytest      # Run tests
poetry run python app.py  # Manual test
```

### 4. Check Changelogs

Before updating, check what changed:
```bash
# For Flask example:
# Visit: https://flask.palletsprojects.com/changes/
```

### 5. Use Lock File for Safety

The `poetry.lock` file is your safety net:

```bash
# Update went wrong? Revert!
git checkout poetry.lock
poetry install  # Goes back to previous versions
```

## Common Update Scenarios

### Scenario 1: Security Patch

```bash
# CVE found in Werkzeug 3.0.1, patch in 3.0.2
poetry add werkzeug@3.0.2
poetry run pytest
# Deploy immediately
```

### Scenario 2: New Feature You Want

```bash
# Flask 3.1.0 has a feature you want
poetry show --outdated
poetry update flask --dry-run  # Check conflicts
poetry update flask
poetry run pytest
```

### Scenario 3: Dependency Conflict

```bash
# You want to add a package but it conflicts
poetry add some-new-package

# Error: Conflicts with flask-sqlalchemy
# Solution: Update the conflicting package
poetry add flask-sqlalchemy@latest
# Or find a compatible version
poetry add some-new-package@2.0.0
```

### Scenario 4: Start Fresh

```bash
# Nuclear option: recreate environment
poetry env remove python
rm poetry.lock
poetry install
# This gets latest compatible versions
```

## Summary Commands

```bash
# Check for updates
poetry show --outdated

# Preview updates
poetry update --dry-run

# Update one package
poetry update flask

# Update everything
poetry update

# Update to specific version
poetry add flask@3.1.0

# Update to latest
poetry add flask@latest

# See what changed
poetry show flask
```

## Pro Tips 💡

### Tip 1: Lock File is Your Friend

Always commit `poetry.lock` to Git. If an update breaks something:

```bash
git diff poetry.lock  # See what changed
git checkout HEAD~1 poetry.lock  # Go back one commit
poetry install  # Restore previous versions
```

### Tip 2: Separate Dev Dependencies

Dev tools can be updated more freely:

```bash
# Update dev dependencies separately
poetry update --only dev
```

### Tip 3: Check Compatibility Matrix

Some packages are tightly coupled:

```
Flask-SQLAlchemy 3.1.x requires SQLAlchemy >=2.0
Flask-Login 0.6.x works with Flask 1.0-3.x
```

Poetry handles this automatically!

### Tip 4: Watch Poetry's Output

Poetry tells you what it's doing:

```
Resolving dependencies...
  • flask requires werkzeug (>=3.0.0)
  • Checking if werkzeug 3.1.5 is compatible
  • ✓ werkzeug 3.1.5 is compatible
```

Read this! It shows you how dependencies are resolved.

---

**Bottom Line:** Poetry makes updating easy and safe. Start with `poetry show --outdated`, test with `--dry-run`, then update one package at a time for peace of mind.
