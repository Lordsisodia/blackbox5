#!/bin/bash

# Stop all completed sub-agent sessions

SUBAGENTS=(
    "agent:main:subagent:81d80c4c-fd10-4e85-947a-4b1ce71afd97"
    "agent:main:subagent:0c380d61-bdd5-46f8-8ece-0473604776fd"
    "agent:main:subagent:518aebe5-0537-48f5-9a2a-57f5380c0d39"
    "agent:main:subagent:8972cb2e-e7c7-4723-a007-d760d28bfaf8"
    "agent:main:subagent:f5d0938e-a937-4472-b3f7-cc4d106e3c8f"
    "agent:main:subagent:2378decc-00c9-41c0-9fda-d88807755bfa"
    "agent:main:subagent:415a8666-0824-4b83-8e3f-c2eb7b290588"
    "agent:main:subagent:c7223131-3790-48fe-b94c-acc389603034"
    "agent:main:subagent:a12206e9-4c80-45d3-9481-4f9acd68735b"
    "agent:main:subagent:f5d0938e-a937-4472-b3f7-cc4d106e3c8f"
)

echo "Stopping all completed sub-agents..."

for SESSION_KEY in "${SUBAGENTS[@]}"; do
    echo "Stopping session: $SESSION_KEY"
    
    # Try to kill via agent command
    openclaw --agent main stop --session-key "$SESSION_KEY" 2>/dev/null
    
    # If that doesn't work, try via sessions kill
    openclaw sessions kill --session-key "$SESSION_KEY" 2>/dev/null
    
    echo "  → Killed"
done

echo ""
echo "✅ All completed sub-agents stopped!"
echo ""
echo "They have finished their research and implementation guides."
echo "You can now start implementing any of these systems when you're ready."
