#!/bin/bash
# ============================================================================
# BlackBox5 GitHub Integration Setup Script
# ============================================================================
# Purpose: Set up GitHub integration for BlackBox5 autonomous development
# ============================================================================

set -e

echo "=========================================="
echo "BlackBox5 GitHub Integration Setup"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo -e "${RED}ERROR: GitHub CLI (gh) is not installed${NC}"
    echo "Install it from: https://cli.github.com/"
    exit 1
fi

echo -e "${GREEN}✓${NC} GitHub CLI found"

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo -e "${YELLOW}⚠${NC} Not authenticated to GitHub"
    echo "Run: gh auth login"
    exit 1
fi

echo -e "${GREEN}✓${NC} Authenticated to GitHub"

# Get repository info
REPO=$(git remote get-url origin 2>/dev/null || echo "not a git repo")
echo -e "${GREEN}✓${NC} Repository: $REPO"

# Check for existing secrets
echo ""
echo "Checking for existing GitHub secrets..."

if gh secret list --json name | grep -q "GITHUB_TOKEN"; then
    echo -e "${YELLOW}⚠${NC} GITHUB_TOKEN secret already exists"
else
    echo -e "${GREEN}✓${NC} GITHUB_TOKEN secret not set (will need to add)"
fi

# Create secrets file for local use
SECRET_FILE="$HOME/.secrets/github_token"
mkdir -p "$(dirname "$SECRET_FILE")"

if [ -f "$SECRET_FILE" ]; then
    echo -e "${GREEN}✓${NC} Local token file exists: $SECRET_FILE"
else
    echo -e "${YELLOW}⚠${NC} Local token file not found"
    echo ""
    echo "To create a GitHub Personal Access Token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Click 'Generate new token' → 'Generate new token (classic)'"
    echo "3. Select scopes: repo, workflow, project"
    echo "4. Save the token to: $SECRET_FILE"
    echo ""
    read -p "Do you want to create the token file now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -sp "Enter your GitHub token: " TOKEN
        echo
        echo "$TOKEN" > "$SECRET_FILE"
        chmod 600 "$SECRET_FILE"
        echo -e "${GREEN}✓${NC} Token saved to $SECRET_FILE"
    fi
fi

# Add token to repository secrets
echo ""
read -p "Do you want to add GITHUB_TOKEN to repository secrets? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    TOKEN=$(cat "$SECRET_FILE")
    gh secret set GITHUB_TOKEN --body "$TOKEN"
    echo -e "${GREEN}✓${NC} GITHUB_TOKEN secret added to repository"
fi

# Check for GitHub Project
echo ""
echo "Checking for GitHub Project..."

PROJECTS=$(gh project list --owner Lordsisodia 2>/dev/null || echo "")

if echo "$PROJECTS" | grep -qi "blackbox5"; then
    echo -e "${GREEN}✓${NC} BlackBox5 project found"
else
    echo -e "${YELLOW}⚠${NC} No BlackBox5 project found"
    echo ""
    read -p "Do you want to create a GitHub Project now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        gh project create --owner Lordsisodia --title "BlackBox5 Development" --template "board"
        echo -e "${GREEN}✓${NC} Project created"
    fi
fi

# Enable GitHub Actions
echo ""
echo "Checking GitHub Actions..."

if gh api repos/Lordsisodia/blackbox5/actions/permissions &> /dev/null; then
    echo -e "${GREEN}✓${NC} GitHub Actions are enabled"
else
    echo -e "${YELLOW}⚠${NC} GitHub Actions may not be enabled"
    echo "Check repository settings → Actions → General"
fi

# Make scripts executable
echo ""
echo "Making integration scripts executable..."

SCRIPTS=(
    "bin/sync_tasks_to_github.py"
    "bin/generate_api_docs.py"
    "bin/generate_module_index.py"
    "bin/update_readme_toc.py"
    "bin/sync_to_project_board.py"
)

for script in "${SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        chmod +x "$script"
        echo -e "${GREEN}✓${NC} Made executable: $script"
    else
        echo -e "${YELLOW}⚠${NC} Script not found: $script"
    fi
done

# Test workflows
echo ""
echo "Testing workflows..."

for workflow in .github/workflows/*.yml; do
    if [ -f "$workflow" ]; then
        echo -e "${GREEN}✓${NC} Workflow found: $(basename "$workflow")"
    fi
done

# Summary
echo ""
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next Steps:"
echo "1. Verify GITHUB_TOKEN secret is set"
echo "2. Create a GitHub Project board (if not done)"
echo "3. Update PROJECT_NUMBER in bin/sync_to_project_board.py"
echo "4. Run a test sync: python bin/sync_tasks_to_github.py"
echo ""
echo "Documentation:"
echo "  See: 1-docs/04-project/GITHUB-INTEGRATION.md"
echo ""
