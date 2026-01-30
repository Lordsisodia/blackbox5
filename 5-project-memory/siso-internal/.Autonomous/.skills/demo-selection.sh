#!/bin/bash
# Skill Selection Demonstration
# Shows how Legacy would select skills based on task context

SKILLS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
INDEX_FILE="$SKILLS_DIR/skills-index.yaml"

echo "========================================"
echo "Legacy Skill Selection Demo"
echo "========================================"
echo ""

# Function to calculate trigger score
calculate_score() {
    local task="$1"
    local skill="$2"
    local score=0

    # Get keywords for skill
    local keywords=$(grep -A20 "id: $skill" "$INDEX_FILE" | grep "keywords:" | sed 's/.*\[//;s/\].*//;s/,//g;s/"//g')

    # Check each keyword
    for keyword in $keywords; do
        if echo "$task" | grep -qi "$keyword"; then
            score=$((score + 10))
            echo "    +10 for keyword: '$keyword'"
        fi
    done

    echo "  Total score: $score"
    return $score
}

# Demo 1: Implementation task
echo "Demo 1: Implementation Task"
echo "---------------------------"
echo "Task: 'Implement user authentication with OAuth'"
echo ""
echo "Matching skills:"

for skill in code-implementation deep-research architecture-design; do
    echo ""
    echo "  Skill: $skill"
    calculate_score "implement user authentication" "$skill"
done

echo ""
echo "→ Selected: code-implementation (highest score)"
echo ""

# Demo 2: Research task
echo "Demo 2: Research Task"
echo "---------------------"
echo "Task: 'Research state management options for React'"
echo ""
echo "Matching skills:"

for skill in deep-research architecture-design product-planning; do
    echo ""
    echo "  Skill: $skill"
    calculate_score "research state management" "$skill"
done

echo ""
echo "→ Selected: deep-research (highest score)"
echo ""

# Demo 3: Database task
echo "Demo 3: Database Task"
echo "---------------------"
echo "Task: 'Create users table with RLS policies'"
echo ""
echo "Matching skills:"

for skill in supabase-operations code-implementation testing-validation; do
    echo ""
    echo "  Skill: $skill"
    calculate_score "create table RLS" "$skill"
done

echo ""
echo "→ Selected: supabase-operations (highest score)"
echo ""

echo "========================================"
echo "Demo Complete"
echo "========================================"
echo ""
echo "The skill selection system:"
echo "1. Reads skills-index.yaml"
echo "2. Matches task keywords against skill triggers"
echo "3. Scores each match (keyword=10pts, context=5pts)"
echo "4. Selects highest scoring skill"
echo "5. Loads and executes the skill"
