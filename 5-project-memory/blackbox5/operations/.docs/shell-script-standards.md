# Shell Script Standards

**Version:** 1.0.0
**Last Updated:** 2026-02-01
**Purpose:** Establish quality standards for shell scripts in BlackBox5

---

## Overview

All shell scripts in BlackBox5 must pass shellcheck validation before being committed. This ensures code quality, prevents common errors, and maintains consistency across the codebase.

---

## Shellcheck Integration

### CI/CD Pipeline

Shellcheck runs automatically on every push and pull request via `.github/workflows/ci.yml`:

```yaml
shellcheck:
  name: Shell Script Analysis
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-shellcheck@v2
    - name: Check shell scripts
      run: shellcheck bin/*.sh ...
```

### Local Testing

Install shellcheck:
```bash
# Ubuntu/Debian
sudo apt-get install shellcheck

# macOS
brew install shellcheck
```

Run shellcheck locally:
```bash
# Check all bin/ scripts
shellcheck bin/*.sh

# Check specific script
shellcheck path/to/script.sh
```

---

## Mandatory Standards

### 1. Shebang and Shell Declaration

All scripts must start with a shebang:

```bash
#!/bin/bash   # For Bash-specific scripts
#!/bin/sh     # For POSIX-compliant scripts
```

**Rule:** Use `#!/bin/bash` if you use Bash-specific features (arrays, `[[ ]]`, etc.).
**Rule:** Use `#!/bin/sh` for maximum portability when only POSIX features are needed.

### 2. Quote Variables

Always quote variables to prevent word splitting and globbing:

```bash
# BAD
if [ -z $var ]; then
    echo $filename
fi

# GOOD
if [ -z "$var" ]; then
    echo "$filename"
fi
```

**Exception:** Omit quotes when you specifically want word splitting (e.g., arrays).

### 3. Use `[[ ]]` for Bash Tests

For Bash scripts, use `[[ ]]` instead of `[ ]` or `test`:

```bash
# GOOD (Bash)
if [[ -z "$var" ]]; then
    ...
fi

# GOOD (POSIX sh)
if [ -z "$var" ]; then
    ...
fi
```

### 4. Use `$()` Instead of Backticks

Use modern command substitution syntax:

```bash
# BAD
CURRENT_DIR=$(pwd)

# GOOD
CURRENT_DIR=`pwd`
```

### 5. Avoid Useless Cat

Use input redirection instead of piping from `cat`:

```bash
# BAD
cat file.txt | command

# GOOD
command < file.txt
# OR
command file.txt
```

### 6. Use `set -e` for Error Handling

Enable exit on error for critical scripts:

```bash
#!/bin/bash
set -e  # Exit on error
set -u  # Exit on undefined variable
set -o pipefail  # Exit on pipe failure
```

### 7. Use Functions for Reusability

Organize code into functions:

```bash
#!/bin/bash

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

main() {
    log_info "Starting..."
    log_error "Something went wrong"
}

main "$@"
```

### 8. Proper Exit Codes

Always return meaningful exit codes:

```bash
# 0 = Success
# 1 = General error
# 2 = Misuse of shell command
# 126 = Command invoked cannot execute
# 127 = Command not found
# 130 = Ctrl+C interrupt

if [[ -f "$required_file" ]]; then
    exit 0
else
    echo "Error: Required file not found" >&2
    exit 1
fi
```

---

## Common Shellcheck Warnings

### SC2046: Quote this to prevent word splitting

**Problem:** Unquoted command substitution
```bash
# BAD
git pull origin $(git branch --show-current)

# GOOD
git pull origin "$(git branch --show-current)"
```

### SC2002: Useless cat

**Problem:** Piping from `cat` unnecessarily
```bash
# BAD
cat file.txt | command

# GOOD
command < file.txt
```

### SC2086: Double quote to prevent globbing

**Problem:** Unquoted variable in expansion context
```bash
# BAD
lsof -Pi :$port

# GOOD
lsof -Pi :"$port"
```

### SC2064: Use single quotes for trap

**Problem:** Variables in trap expand when defined, not when triggered
```bash
# BAD
trap "echo $PID; kill $PID" SIGINT

# GOOD
trap 'echo $PID; kill $PID' SIGINT
```

### SC2236: Use -n instead of ! -z

**Problem:** Negated test for non-empty string
```bash
# BAD
if [ ! -z "$var" ]; then

# GOOD
if [ -n "$var" ]; then
```

### SC2034: Variable appears unused

**Problem:** Defined but never used
```bash
# BAD
YELLOW='\033[1;33m'  # Never used
# Remove unused variables or export if used externally
```

---

## File Organization

### Script Structure Template

```bash
#!/bin/bash
# ============================================================================
# Script Name
# ============================================================================
# Purpose: Brief description of what the script does
# Usage: ./script.sh [options]
# Author: Your Name
# ============================================================================

set -euo pipefail

# ============================================================================
# CONFIGURATION
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# ============================================================================
# FUNCTIONS
# ============================================================================

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# ============================================================================
# MAIN
# ============================================================================

main() {
    log_info "Starting..."
    # Your logic here
    log_success "Done!"
}

main "$@"
```

---

## Pre-Commit Hook (Optional)

Add shellcheck to your pre-commit hooks for immediate feedback:

**`.git/hooks/pre-commit`:**
```bash
#!/bin/bash
# Pre-commit hook for shellcheck

echo "Running shellcheck..."

# Check all .sh files
if ! shellcheck bin/*.sh legacy-codespace-loop.sh 5-project-memory/blackbox5/.autonomous/ralf-daemon.sh; then
    echo "Shellcheck failed. Please fix errors before committing."
    exit 1
fi

echo "Shellcheck passed!"
```

Enable it:
```bash
chmod +x .git/hooks/pre-commit
```

---

## Testing

### Manual Testing Checklist

Before committing a shell script:

- [ ] Script passes `shellcheck` with no errors
- [ ] Script is executable (`chmod +x script.sh`)
- [ ] Script has proper shebang (`#!/bin/bash` or `#!/bin/sh`)
- [ ] All variables are quoted
- [ ] Error handling is in place (`set -e`)
- [ ] Exit codes are meaningful
- [ ] Script has been tested manually
- [ ] Documentation is clear (usage, options, examples)

### Automated Testing

```bash
# Run shellcheck on all shell scripts
find . -name "*.sh" -type f -exec shellcheck {} \;

# Exit with error if any script fails
! find . -name "*.sh" -type f -exec shellcheck {} + | grep -q "^[^:]*:[0-9]*:"
```

---

## Resources

- [Shellcheck Online](https://www.shellcheck.net/) - Test scripts online
- [Shellcheck Wiki](https://github.com/koalaman/shellcheck/wiki) - Full warning reference
- [Bash Style Guide](https://google.github.io/styleguide/shellguide.html) - Google's shell scripting guidelines
- [POSIX Shell Reference](https://pubs.opengroup.org/onlinepubs/9699919799/utilities/V3_chap02.html) - POSIX standard

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-01 | Initial version - Shellcheck CI/CD integration, standards documented |
