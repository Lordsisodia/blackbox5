#!/bin/bash
# Create all SISO Research Organization repos on GitHub
# Usage: ./create-siso-repos.sh

REPOS=(
  "youtube-ai-research:YouTube AI Research:YouTube video scraping and analysis system"
  "siso-engine:SISO Engine:Core agent runtime and RALF system"
  "siso-cli:SISO CLI:Command-line tools for BlackBox5"
  "siso-research-bank:SISO Research Bank:Research projects and data"
  "siso-internal-memory:SISO Internal Memory:Project memory for SISO Internal"
  "blackbox5-memory:BlackBox5 Memory:Project memory for BlackBox5"
  "team-entrepreneurship-memory:Team Entrepreneurship Memory:Project memory for team projects"
)

echo "Creating SISO Research Organization repos..."
echo "Make sure you're logged in: gh auth login"
echo ""

for repo_info in "${REPOS[@]}"; do
  IFS=':' read -r repo name description <<< "$repo_info"

  echo "Creating: $repo"
  echo "  Name: $name"
  echo "  Description: $description"

  gh repo create "lordsisodia/$repo" \
    --public \
    --description "$description" \
    --source="." \
    --remote="origin" \
    --push

  if [ $? -eq 0 ]; then
    echo "  ✓ Created successfully"
  else
    echo "  ✗ Failed to create (may already exist)"
  fi
  echo ""
done

echo "Done! Next steps:"
echo "1. Add MIRROR_TOKEN secret to BlackBox5 repo"
echo "2. Push BlackBox5 to trigger initial mirrors"
echo "3. Check each repo for README setup"
