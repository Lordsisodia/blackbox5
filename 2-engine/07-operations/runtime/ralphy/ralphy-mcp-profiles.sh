#!/usr/bin/env bash
# ============================================
# Ralphy MCP Profile Manager
# ============================================
# Manages different MCP configuration profiles for Ralphy
# based on task requirements and agent capabilities.
#
# Profiles:
#   - minimal:    No MCP servers (fastest, for pure coding)
#   - filesystem: Filesystem access only
#   - standard:   Common MCPs (filesystem, fetch, search)
#   - full:       All available MCPs (slowest, most capable)
#
# Usage:
#   ralphy-mcp-profiles.sh init              # Set up profile system
#   ralphy-mcp-profiles.sh list             # List available profiles
#   ralphy-mcp-profiles.sh current          # Show current profile
#   ralphy-mcp-profiles.sh use <profile>    # Switch to profile
#   ralphy-mcp-profiles.sh detect <task>    # Auto-detect best profile
# ============================================

set -euo pipefail

# ============================================
# CONFIGURATION
# ============================================

VERSION="1.0.0"
PROFILES_DIR="${HOME}/.claude-profiles"
ACTIVE_PROFILE_FILE="${PROFILES_DIR}/.active"
SYSTEM_CLAUDE_CONFIG="${HOME}/.config/claude/config.json"

# Colors
if [[ -t 1 ]] && command -v tput &>/dev/null && [[ $(tput colors 2>/dev/null || echo 0) -ge 8 ]]; then
  RED=$(tput setaf 1)
  GREEN=$(tput setaf 2)
  YELLOW=$(tput setaf 3)
  BLUE=$(tput setaf 4)
  CYAN=$(tput setaf 6)
  BOLD=$(tput bold)
  RESET=$(tput sgr0)
else
  RED="" GREEN="" YELLOW="" BLUE="" CYAN="" BOLD="" RESET=""
fi

# ============================================
# MCP PROFILE DEFINITIONS
# ============================================

# Profile: minimal - No MCP servers (fastest)
profile_minimal() {
  cat <<'EOF'
{
  "mcpServers": {}
}
EOF
}

# Profile: filesystem - Only filesystem access
profile_filesystem() {
  cat <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${HOME}"]
    }
  }
}
EOF
}

# Profile: standard - Common lightweight MCPs
profile_standard() {
  cat <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${HOME}"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@h16rkim/mcp-fetch-server"]
    },
    "duckduckgo": {
      "command": "npx",
      "args": ["-y", "duckduckgo-mcp-server"]
    }
  }
}
EOF
}

# Profile: data - Data and documentation MCPs
profile_data() {
  cat <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${HOME}"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@h16rkim/mcp-fetch-server"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "wikipedia": {
      "command": "npx",
      "args": ["-y", "@shiquda/mediawiki-mcp-server"]
    }
  }
}
EOF
}

# Profile: automation - Browser and automation MCPs
profile_automation() {
  cat <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${HOME}"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@chrome-devtools/mcp-server"]
    }
  }
}
EOF
}

# Profile: full - All available MCPs from system config
profile_full() {
  # Read from existing system config if available
  if [[ -f "$SYSTEM_CLAUDE_CONFIG" ]]; then
    cat "$SYSTEM_CLAUDE_CONFIG"
  else
    # Fallback to comprehensive set
    cat <<EOF
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "${HOME}"]
    },
    "fetch": {
      "command": "npx",
      "args": ["-y", "@h16rkim/mcp-fetch-server"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@executeautomation/playwright-mcp-server"]
    },
    "chrome-devtools": {
      "command": "npx",
      "args": ["-y", "@chrome-devtools/mcp-server"]
    },
    "context7": {
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    },
    "duckduckgo": {
      "command": "npx",
      "args": ["-y", "duckduckgo-mcp-server"]
    },
    "wikipedia": {
      "command": "npx",
      "args": ["-y", "@shiquda/mediawiki-mcp-server"]
    },
    "serena": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/oraios/serena", "serena-mcp-server"]
    }
  }
}
EOF
  fi
}

# ============================================
# TASK DETECTION RULES
# ============================================

# Analyze task description and recommend profile
detect_profile_for_task() {
  local task="$1"
  task=$(echo "$task" | tr '[:upper:]' '[:lower:]')

  # Keywords that trigger different profiles
  local automation_keywords=("browser" "scrape" "screenshot" "web" "chrome" "playwright" "headless" "puppeteer")
  local data_keywords=("search" "documentation" "docs" "wikipedia" "research" "context" "reference" "lookup")
  local standard_keywords=("fetch" "http" "api" "url" "download" "webhook")

  # Check for automation needs
  for keyword in "${automation_keywords[@]}"; do
    if [[ "$task" == *"$keyword"* ]]; then
      echo "automation"
      return
    fi
  done

  # Check for data/research needs
  for keyword in "${data_keywords[@]}"; do
    if [[ "$task" == *"$keyword"* ]]; then
      echo "data"
      return
    fi
  done

  # Check for standard needs
  for keyword in "${standard_keywords[@]}"; do
    if [[ "$task" == *"$keyword"* ]]; then
      echo "standard"
      return
    fi
  done

  # Default to minimal for pure coding tasks
  echo "minimal"
}

# ============================================
# UTILITY FUNCTIONS
# ============================================

log_info() { echo "${BLUE}[INFO]${RESET} $*"; }
log_success() { echo "${GREEN}[OK]${RESET} $*"; }
log_warn() { echo "${YELLOW}[WARN]${RESET} $*"; }
log_error() { echo "${RED}[ERROR]${RESET} $*" >&2; }

# Get profile description
get_profile_description() {
  local profile="$1"
  case "$profile" in
    minimal)
      echo "No MCP servers - fastest startup, pure coding only"
      ;;
    filesystem)
      echo "Filesystem access - for file operations"
      ;;
    standard)
      echo "Common MCPs - filesystem, fetch, search"
      ;;
    data)
      echo "Data & docs - filesystem, fetch, context7, wikipedia"
      ;;
    automation)
      echo "Browser automation - filesystem, playwright, chrome-devtools"
      ;;
    full)
      echo "All MCPs - slowest startup, maximum capability"
      ;;
    *)
      echo "Unknown profile"
      ;;
  esac
}

# List all available profiles
list_profiles() {
  echo "${BOLD}Available MCP Profiles:${RESET}"
  echo
  printf "%-15s %s\n" "Profile" "Description"
  printf "%-15s %s\n" "-------" "-----------"
  printf "%-15s %s\n" "minimal" "$(get_profile_description minimal)"
  printf "%-15s %s\n" "filesystem" "$(get_profile_description filesystem)"
  printf "%-15s %s\n" "standard" "$(get_profile_description standard)"
  printf "%-15s %s\n" "data" "$(get_profile_description data)"
  printf "%-15s %s\n" "automation" "$(get_profile_description automation)"
  printf "%-15s %s\n" "full" "$(get_profile_description full)"
  echo
}

# Show current active profile
show_current_profile() {
  if [[ -f "$ACTIVE_PROFILE_FILE" ]]; then
    local current
    current=$(cat "$ACTIVE_PROFILE_FILE")
    echo "${BOLD}Current Profile:${RESET} ${CYAN}${current}${RESET}"
    echo "Description: $(get_profile_description "$current")"
    echo "Config: ${PROFILES_DIR}/${current}/config.json"
  else
    log_warn "No active profile set (using system default)"
    echo "System config: $SYSTEM_CLAUDE_CONFIG"
  fi
}

# ============================================
# CORE COMMANDS
# ============================================

# Initialize profile system
cmd_init() {
  log_info "Initializing Ralphy MCP Profile System..."

  mkdir -p "$PROFILES_DIR"

  # Create default profile configs
  for profile in minimal filesystem standard data automation full; do
    local profile_dir="${PROFILES_DIR}/${profile}"
    mkdir -p "$profile_dir"

    case "$profile" in
      minimal) profile_minimal > "${profile_dir}/config.json" ;;
      filesystem) profile_filesystem > "${profile_dir}/config.json" ;;
      standard) profile_standard > "${profile_dir}/config.json" ;;
      data) profile_data > "${profile_dir}/config.json" ;;
      automation) profile_automation > "${profile_dir}/config.json" ;;
      full) profile_full > "${profile_dir}/config.json" ;;
    esac

    log_success "Created profile: ${profile}"
  done

  # Set minimal as default
  echo "minimal" > "$ACTIVE_PROFILE_FILE"

  log_success "Profile system initialized at: $PROFILES_DIR"
  echo
  echo "Usage:"
  echo "  export CLAUDE_CONFIG_DIR=\"$PROFILES_DIR/\$(cat $ACTIVE_PROFILE_FILE)\""
}

# Switch to a profile
cmd_use() {
  local profile="$1"

  if [[ -z "$profile" ]]; then
    log_error "Usage: $0 use <profile>"
    exit 1
  fi

  # Check if profile exists
  if [[ ! -d "${PROFILES_DIR}/${profile}" ]]; then
    log_error "Profile '$profile' not found"
    echo "Available profiles: minimal, filesystem, standard, data, automation, full"
    exit 1
  fi

  # Set as active
  echo "$profile" > "$ACTIVE_PROFILE_FILE"

  log_success "Switched to profile: ${profile}"
  echo "Description: $(get_profile_description "$profile")"
  echo
  echo "To use with Ralphy:"
  echo "  export CLAUDE_CONFIG_DIR=\"$PROFILES_DIR/${profile}\""
}

# Auto-detect profile for task
cmd_detect() {
  local task="$1"

  if [[ -z "$task" ]]; then
    log_error "Usage: $0 detect \"<task description>\""
    exit 1
  fi

  local detected
  detected=$(detect_profile_for_task "$task")

  log_info "Task: $task"
  echo
  log_success "Recommended profile: ${CYAN}${detected}${RESET}"
  echo "Reason: $(get_profile_description "$detected")"
  echo
  echo "To use this profile:"
  echo "  export CLAUDE_CONFIG_DIR=\"$PROFILES_DIR/${detected}\""
}

# Export for Ralphy
cmd_export() {
  local profile="${1:-}"

  # If no profile specified, use active
  if [[ -z "$profile" ]]; then
    if [[ -f "$ACTIVE_PROFILE_FILE" ]]; then
      profile=$(cat "$ACTIVE_PROFILE_FILE")
    else
      profile="minimal"
    fi
  fi

  local config_dir="${PROFILES_DIR}/${profile}"

  if [[ ! -d "$config_dir" ]]; then
    log_error "Profile '$profile' not found. Run '$0 init' first."
    exit 1
  fi

  echo "export CLAUDE_CONFIG_DIR=\"$config_dir\""
}

# Show help
cmd_help() {
  cat <<EOF
${BOLD}Ralphy MCP Profile Manager v${VERSION}${RESET}

Manages different MCP configuration profiles for Ralphy.

${BOLD}Usage:${RESET}
  $0 <command> [args]

${BOLD}Commands:${RESET}
  ${CYAN}init${RESET}              Initialize profile system (creates configs)
  ${CYAN}list${RESET}              List available profiles
  ${CYAN}current${RESET}           Show current active profile
  ${CYAN}use <profile>${RESET}     Switch to a profile
  ${CYAN}detect <task>${RESET}     Auto-detect best profile for task
  ${CYAN}export [profile]${RESET}  Export CLAUDE_CONFIG_DIR variable
  ${CYAN}help${RESET}              Show this help message

${BOLD}Examples:${RESET}
  # Initialize the system
  $0 init

  # List all profiles
  $0 list

  # Switch to automation profile
  $0 use automation

  # Auto-detect profile for a task
  $0 detect "Create a web scraper using playwright"

  # Use with Ralphy
  eval $($0 export minimal)
  ralphy.sh --prd PRD.md

${BOLD}Profiles:${RESET}
  minimal       No MCP servers (fastest)
  filesystem    Filesystem access only
  standard      Common lightweight MCPs
  data          Data & documentation MCPs
  automation    Browser & automation MCPs
  full          All available MCPs (slowest)

${BOLD}Integration with Ralphy:${RESET}
  # Method 1: Export before running
  eval $($0 export minimal)
  ralphy.sh --prd PRD.md

  # Method 2: One-liner
  CLAUDE_CONFIG_DIR=\"$PROFILES_DIR/minimal\" ralphy.sh --prd PRD.md

  # Method 3: Auto-detect from PRD
  PROFILE=$($0 detect "$(head -20 PRD.md)" | grep Recommended | awk '{print \$NF}')
  CLAUDE_CONFIG_DIR=\"$PROFILES_DIR/\$PROFILE\" ralphy.sh --prd PRD.md
EOF
}

# ============================================
# MAIN
# ============================================

main() {
  local command="${1:-help}"
  shift || true

  case "$command" in
    init) cmd_init ;;
    list) list_profiles ;;
    current) show_current_profile ;;
    use) cmd_use "$@" ;;
    detect) cmd_detect "$@" ;;
    export) cmd_export "$@" ;;
    help|--help|-h) cmd_help ;;
    *)
      log_error "Unknown command: $command"
      echo "Run '$0 help' for usage information"
      exit 1
      ;;
  esac
}

main "$@"
