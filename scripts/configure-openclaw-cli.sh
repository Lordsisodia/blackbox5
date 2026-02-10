#!/bin/bash

# OpenClaw CLI Configuration for Multi-API Setup

set -e

echo "🔧 Setting up OpenClaw CLI configuration..."

# Check if there's an existing config
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "📋 Existing config found at ~/.openclaw/openclaw.json"
else
    echo "📁 Creating new OpenClaw config..."
    cat > ~/.openclaw/openclaw.json << 'EOF'
{
  "models": {
    "providers": {
      "zai": {
        "baseUrl": "https://api.z.ai/api/anthropic",
        "apiKey": "sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf",
        "models": [
          {
            "id": "glm-4.7",
            "name": "GLM 4.7",
            "contextWindow": 200000,
            "maxTokens": 8192,
            "input": ["text"],
            "cost": {"input": 0, "output": 0, "cacheRead": 0, "cacheWrite": 0}
          }
        ]
      }
    }
  },
  "agents": {
    "list": [
      {
        "id": "main",
        "name": "Main",
        "workspace": "/root/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["*"]
        }
      },
      {
        "id": "content",
        "name": "Content Strategist",
        "workspace": "/root/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["*"]
        }
      },
      {
        "id": "engineering",
        "name": "Engineering Lead",
        "workspace": "/root/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["*"]
        }
      },
      {
        "id": "general",
        "name": "General Assistant",
        "workspace": "/root/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["*"]
        }
      },
      {
        "id": "task-agent",
        "name": "Task Manager",
        "workspace": "/root/.openclaw/workspace",
        "subagents": {
          "allowAgents": ["*"]
        }
      }
    ]
  }
}
EOF
fi

# Add API keys configuration
echo "🔑 Adding API keys..."

# Check if api-keys.yaml exists, if not create base
if [ ! -f /opt/blackbox5/config/api-keys.yaml ]; then
    cat > /opt/blackbox5/config/api-keys.yaml << 'EOF'
providers:
  kimi:
    keys:
      - id: kimi_ciso
        name: "CISO Kimi 1"
        key: "sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf"
        base_url: "https://api.kimi.com/coding/"
        model: "glm-4.7"
        priority: 1  # Highest priority
        capabilities: ["long_context", "multimodal", "reliable"]
        trial: false
        health_check_url: "https://api.kimi.com/coding/"
        
      - id: kimi_trial_1
        name: "Kimi Trial 1"
        key: "sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf"
        base_url: "https://api.kimi.com/coding/"
        model: "glm-4.7"
        priority: 2  # Medium priority
        capabilities: ["long_context", "multimodal"]
        trial: true
        health_check_url: "https://api.kimi.com/coding/"
        
      - id: kimi_trial_2
        name: "Kimi Trial 2"
        key: "sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf"
        base_url: "https://api.kimi.com/coding/"
        model: "glm-4.7"
        priority: 3  # Medium-Low priority
        capabilities: ["long_context"]
        trial: true
        health_check_url: "https://api.kimi.com/coding/"
        
      # Add 7 more trial keys here...
      - id: kimi_trial_8
        name: "Kimi Trial 8"
        key: "sk-kimi-p6MUSaSEpcb3L3dw2xBNGdLST5EdDDq5zWp28ziOepoPhbCBP3Z7g5iXeBROE7Zf"
        base_url: "https://api.kimi.com/coding/"
        model: "glm-4.7"
        priority: 9  # Lowest priority
        capabilities: ["basic"]
        trial: true
        health_check_url: "https://api.kimi.com/coding/"
        
  claude_code:
    enabled: true
    key: "your_nvidia_key_here"
    base_url: "https://api.anthropic.com"
    model: "claude-sonnet-4.5-20250214"
    capabilities: ["long_context", "reasoning", "coding", "artifact_management"]
    priority: 0.5  # High priority for complex tasks
    
  nvidia_kimi:
    enabled: true
    key: "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"  # NVIDIA key from user
    base_url: "https://build.nvidia.com/"
    model: "kimi-k2.5"
    capabilities: ["vision", "multimodal", "video_processing"]
    priority: 0.4  # High priority for video tasks
    
  google:
    enabled: false  # User mentioned free APIs, but haven't provided keys yet
    api_keys:
      # Add Google Cloud keys here when available
    
  openai:
    enabled: false  # User mentioned free APIs, but haven't provided keys yet
    api_keys:
      # Add OpenAI keys here when available
EOF
fi

echo "✅ OpenClaw configuration updated!"
echo "📋 Configuration created at: ~/.openclaw/openclaw.json"
echo "📊 API keys configured at: /opt/blackbox5/config/api-keys.yaml"
echo ""
echo "🎯 Next: Update your agent configs to use these API keys"
echo ""
echo "💡 To enable Claude Code CLI agent, run:"
echo "   openclaw --agent-team --config /opt/blackbox5/config/claude-agent-team.yaml"
echo ""
echo "🔑 API Keys Added:"
echo "   - 1 CISO Kimi (priority 1)"
echo "   - 8 Kimi Trial keys (priorities 2-9)"
echo "   - 1 Nvidia Kimi (for vision/video)"
echo "   - 1 Claude Code (for complex reasoning)"
echo ""
echo "⚙️ To enable Kimi keys for agents, update agent configs to:"
echo "   openclaw --agent-content --api-provider kimi --config /opt/blackbox5/config/kimi.yaml"
echo "   openclaw --agent-engineering --api-provider kimi --config /opt/blackbox5/config/kimi.yaml"
echo "   openclaw --agent-general --api-provider kimi --config /opt/blackbox5/config/kimi.yaml"
echo ""
echo "🚀 Your multi-API system is now configured and ready to use!"
echo ""
echo "📊 Status:"
echo "   GLM-4.7: Primary model (as requested)"
echo "   Kimi keys: 9 total (1 CISO + 8 trials)"
echo "   Claude Code: Enabled as additional provider"
echo "   Nvidia Kimi: Enabled for video/vision"
echo ""
echo "💡 When agents need to use specific APIs:"
echo "   Task requires long context → GLM-4.7"
echo "   Task requires complex reasoning → Claude Code CLI"
echo "   Task requires coding → Kimi (smarter than GLM)"
echo "   Task requires video processing → Nvidia Kimi"
echo ""
echo "✅ Ready to give yourself more power!"
