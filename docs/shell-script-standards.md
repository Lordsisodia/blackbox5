# Shell Script Standards

**Version:** 1.0
**Created:** 2026-02-12
**Purpose:** Standards for writing robust, maintainable shell scripts in BlackBox5

---

## Table of Contents

1. [Script Header](#script-header)
2. [Naming Conventions](#naming-conventions)
3. [Error Handling](#error-handling)
4. [Quoting and Expansion](#quoting-and-expansion)
5. [Variable Declaration](#variable-declaration)
6. [Command Substitution](#command-substitution)
7. [Looping and Iteration](#looping-and-iteration)
8. [Best Practices](#best-practices)
9. [Shellcheck Rules](#shellcheck-rules)
10. [Examples](#examples)

---

## Script Header

Every shell script must start with a shebang and header comment:

```bash
#!/bin/bash
# Script Name: descriptive-name.sh
# Description: Brief description of what the script does
# Author: Your Name or Team
# Created: YYYY-MM-DD
# Usage: ./script-name.sh [options] [arguments]
```

**Rules:**
- Use `#!/bin/bash` for bash scripts (not `#!/bin/sh`)
- Use `set -euo pipefail` for strict error handling
- Include author, date, and usage information

---

## Naming Conventions

### Variables

- **UPPER_CASE**: Constants and global variables
- **lower_case**: Local variables
- **_leading_underscore**: Private/internal variables

```bash
# Good
readonly MAX_RETRIES=3
readonly LOG_FILE="/var/log/app.log"
local retry_count=0
local _internal_state

# Bad
maxRetries=3           # Mixed case
RetryCount=0           # Local variable in UPPER_CASE
__private_state        # Too many underscores
```

### Functions

- **snake_case**: Function names
- **Verb-Noun**: Describe the action

```bash
# Good
get_file_path()
create_backup()
check_dependencies()

# Bad
GetFilePath()          # PascalCase (not bash convention)
CreateBackup()
file_path()            # Not descriptive
```

### Files

- **snake_case.sh**: Script file names
- **kebab-case**: Configuration files (optional)

```bash
# Good
archive-runs.sh
setup-archive-cron.sh

# Bad
ArchiveRuns.sh         # Mixed case
archive_runs.sh         # Underscores (acceptable but snake_case preferred)
```

---

## Error Handling

### Strict Mode

Always enable strict mode:

```bash
set -euo pipefail
```

**What this does:**
- `-e`: Exit on error
- `-u`: Exit on unset variable
- `-o pipefail`: Exit on pipe failure

### Error Checking

Check command exit codes explicitly:

```bash
# Good
if ! command -v git &> /dev/null; then
    error "git is not installed"
    exit 1
fi

# Bad
command -v git &> /dev/null
if [ $? -ne 0 ]; then
    error "git is not installed"
    exit 1
fi
```

### Trap Errors

Use trap for cleanup:

```bash
cleanup() {
    local exit_code=$?
    log "Cleaning up..."
    rm -f "$TEMP_FILE"
    exit $exit_code
}

trap cleanup EXIT INT TERM
```

---

## Quoting and Expansion

### Always Quote Variables

```bash
# Good
echo "$filename"
rm -rf "$directory"
if [ -n "$variable" ]; then

# Bad
echo $filename          # Unsafe if filename contains spaces
rm -rf $directory       # Dangerous!
if [ -n $variable ];   # Fails if variable is empty
```

### Quote Command Substitutions

```bash
# Good
local file_list=$(find /tmp -type f)
local count=$(echo "$file_list" | wc -l)

# Better (declare and assign separately)
local file_list
file_list=$(find /tmp -type f)

# Bad (SC2155 warning)
local file_list=$(find /tmp -type f)
```

### Quote Expansions Separately

```bash
# Good
local path="${root_dir}/subdir"

# Bad (SC2295)
local path="${root_dir/subdir}"
```

### Quote to Prevent Word Splitting

```bash
# Good
files=(*.txt)
for f in "${files[@]}"; do
    process "$f"
done

# Bad (SC2046)
for f in $(ls *.txt); do
    process "$f"
done
```

---

## Variable Declaration

### Local Variables

Always use `local` for function-local variables:

```bash
# Good
process_file() {
    local file_path="$1"
    local temp_dir
    temp_dir=$(mktemp -d)
    # ...
}

# Bad
process_file() {
    file_path="$1"      # Creates global variable
    temp_dir=$(mktemp -d)
    # ...
}
```

### Readonly Variables

Mark constants as readonly:

```bash
readonly MAX_RETRIES=3
readonly CONFIG_FILE="/etc/app/config.yaml"
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
```

### Declare and Assign Separately

```bash
# Good (SC2155)
local file_path
file_path=$(some_command)

# Bad (triggers SC2155 warning)
local file_path=$(some_command)
```

---

## Command Substitution

### Use `$()` Not Backticks

```bash
# Good
local files=$(ls *.txt)
local date=$(date +%Y-%m-%d)

# Bad (obsolete)
local files=`ls *.txt`
local date=`date +%Y-%m-%d`
```

### Use `grep -c` Instead of `grep | wc -l`

```bash
# Good (SC2126)
local count=$(grep -c "pattern" file.txt)

# Bad (inefficient)
local count=$(grep "pattern" file.txt | wc -l)
```

### Use `-print0` for Non-Alphanumeric Filenames

```bash
# Good (SC2038)
find /tmp -type f -print0 | while IFS= read -r -d '' file; do
    process "$file"
done

# Bad (fails on special filenames)
find /tmp -type f | while read file; do
    process "$file"
done
```

---

## Looping and Iteration

### Use `find` Instead of `ls`

```bash
# Good (SC2012)
find /tmp -maxdepth 1 -type f -name "*.txt" | while read file; do
    process "$file"
done

# Bad (SC2012)
ls *.txt | while read file; do
    process "$file"
done
```

### Use Globbing Instead of `ls`

```bash
# Good
for file in *.txt; do
    [ -f "$file" ] || continue
    process "$file"
done

# Bad
for file in $(ls *.txt); do
    process "$file"
done
```

---

## Best Practices

### Avoid Useless `cat`

```bash
# Good
grep "pattern" file.txt
jq . config.json

# Bad (SC2002)
cat file.txt | grep "pattern"
cat config.json | jq .
```

### Avoid Sudo in Redirects

```bash
# Good
sudo cat file | process
echo "content" | sudo tee file > /dev/null

# Bad (SC2024)
sudo echo "content" > file  # Redirect happens as non-root
```

### Use Arrays Instead of Strings

```bash
# Good
local files=("file1.txt" "file2.txt" "file3.txt")
for f in "${files[@]}"; do
    process "$f"
done

# Bad (fails on spaces)
local files="file1.txt file2.txt file3.txt"
for f in $files; do
    process "$f"
done
```

### Combine Redirects

```bash
# Good (SC2129)
{
    echo "First line"
    echo "Second line"
    echo "Third line"
} >> log.txt

# Acceptable
echo "First line" >> log.txt
echo "Second line" >> log.txt
echo "Third line" >> log.txt
```

---

## Shellcheck Rules

### Must Fix (Error)

- **SC2289**: Syntax errors (linefeed in command name)
- **SC2034**: Unused variables (either use them or declare readonly/unused)

### Should Fix (Warning)

- **SC2155**: Declare and assign separately
- **SC2046**: Quote to prevent word splitting
- **SC2064**: Use single quotes in trap signals
- **SC2038**: Use `-print0` or `-exec +` with find
- **SC2181**: Check exit code directly (not `$?`)

### Nice to Fix (Style)

- **SC2002**: Useless cat
- **SC2012**: Use find instead of ls
- **SC2126**: Use `grep -c` instead of `grep | wc -l`
- **SC2129**: Combine redirects
- **SC2207**: Prefer `mapfile` or `read -a` for arrays

---

## Examples

### Complete Script Template

```bash
#!/bin/bash
# Script Name: example-script.sh
# Description: Example script following BlackBox5 standards
# Author: BlackBox5 Team
# Created: 2026-02-12
# Usage: ./example-script.sh [options]

set -euo pipefail

# Configuration
readonly SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
readonly LOG_FILE="/var/log/example.log"
readonly MAX_RETRIES=3

# Logging functions
log() {
    echo -e "\033[0;32m[INFO]\033[0m $1" >&2
}

warn() {
    echo -e "\033[1;33m[WARN]\033[0m $1" >&2
}

error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1" >&2
}

# Cleanup function
cleanup() {
    local exit_code=$?
    log "Cleaning up..."
    rm -f "${TEMP_FILE:-}"
    exit $exit_code
}

trap cleanup EXIT INT TERM

# Main function
main() {
    local file_path="$1"
    local temp_dir
    local retry_count=0

    # Validate input
    if [[ -z "$file_path" ]]; then
        error "File path is required"
        exit 1
    fi

    if [[ ! -f "$file_path" ]]; then
        error "File not found: $file_path"
        exit 1
    fi

    # Create temp directory
    temp_dir=$(mktemp -d)
    log "Created temp directory: $temp_dir"

    # Process file
    log "Processing file: $file_path"
    # ... processing logic ...

    log "Done!"
}

# Run main function
main "$@"
```

### Function Example

```bash
# Good function
get_file_size() {
    local file_path="$1"

    if [[ ! -f "$file_path" ]]; then
        echo "0"
        return 1
    fi

    local size
    size=$(stat -f%z "$file_path" 2>/dev/null || stat -c%s "$file_path" 2>/dev/null)

    echo "$size"
    return 0
}

# Usage
if ! file_size=$(get_file_size "$file"); then
    error "Failed to get file size"
    exit 1
fi

log "File size: $file_size bytes"
```

---

## Resources

- [Shellcheck](https://www.shellcheck.net/)
- [Bash Guide for Beginners](https://tldp.org/LDP/Bash-Beginners-Guide/html/)
- [Advanced Bash-Scripting Guide](https://tldp.org/LDP/abs/html/)
- [Bash FAQ](http://mywiki.wooledge.org/BashFAQ)

---

**Last Updated:** 2026-02-12
**Maintained By:** BlackBox5 Team
