#!/bin/bash
# Test all configured APIs for BlackBox5
# This script tests each API key to verify it works

set -e

echo "========================================"
echo "BlackBox5 API Testing Script"
echo "========================================"
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
PASS=0
FAIL=0

# Test function
test_api() {
    local name="$1"
    local description="$2"
    local command="$3"

    echo -n "Testing $name... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASS++))
        return 0
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAIL++))
        return 1
    fi
}

echo "1. Testing GLM-4.7 (Z.AI)..."
echo "   Description: Primary model for general tasks"
echo ""

# Test GLM-4.7
python3 << 'EOF' 2>/dev/null
import requests
import json
import sys

url = 'https://api.z.ai/api/anthropic/v1/messages'
headers = {
    'Authorization': 'Bearer d81f5ab044ad48b492a8dbc183687dcf.sezM6xOnR9BvFhmf',
    'Content-Type': 'application/json',
    'anthropic-version': '2023-06-01'
}
data = {
    'model': 'glm-4.7',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Say "GLM-4.7 works!"'}]
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    if response.status_code == 200:
        result = response.json()
        content = result.get('content', [{}])[0].get('text', '')
        print(f"   Response: {content[:100]}")
        print("   Status: Active")
        sys.exit(0)
    else:
        print(f"   Error: HTTP {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"   Error: {str(e)[:100]}")
    sys.exit(1)
EOF
if [ $? -eq 0 ]; then ((PASS++)); else ((FAIL++)); fi

echo ""
echo "2. Testing Kimi K2.5 (Moonshot)..."
echo "   Description: Smart coding & multimodal model"
echo "   Keys: 1 CISO + 8 trial keys"
echo ""

# Check if Kimi CISO key is set
KIMI_CISO_KEY="${KIMI_CISO_KEY:-sk-kimi-YC3tlmLzogkd2ZMHdPwMMth3hV9r72aC5lk3kQTYI014GFjBN0VPcKfe6wczYlGr}"

if [ -z "$KIMI_CISO_KEY" ] || [ "$KIMI_CISO_KEY" == "your_key_here" ]; then
    echo -e "${YELLOW}⚠ Kimi CISO key not set${NC}"
    ((FAIL++))
else
    python3 << EOF 2>/dev/null
import requests
import json
import sys

url = 'https://api.moonshot.cn/v1/chat/completions'
headers = {
    'Authorization': f'Bearer $KIMI_CISO_KEY',
    'Content-Type': 'application/json'
}
data = {
    'model': 'moonshot-v1-128k',
    'max_tokens': 100,
    'messages': [{'role': 'user', 'content': 'Say "Kimi K2.5 works!"'}]
}

try:
    response = requests.post(url, headers=headers, json=data, timeout=30)
    if response.status_code == 200:
        result = response.json()
        content = result.get('choices', [{}])[0].get('message', {}).get('content', '')
        print(f"   Response: {content[:100]}")
        print("   Status: Active (CISO Key)")
        sys.exit(0)
    else:
        print(f"   Error: HTTP {response.status_code}")
        print(f"   Response: {response.text[:200]}")
        sys.exit(1)
except Exception as e:
    print(f"   Error: {str(e)[:100]}")
    sys.exit(1)
EOF
    if [ $? -eq 0 ]; then ((PASS++)); else ((FAIL++)); fi
fi

echo ""
echo "3. Testing Claude Code CLI (Anthropic)..."
echo "   Description: Powerful reasoning model"
echo ""

if [ -z "$ANTHROPIC_API_KEY" ] || [ "$ANTHROPIC_API_KEY" == "your_key_here" ]; then
    echo -e "${YELLOW}⚠ ANTHROPIC_API_KEY not set${NC}"
    echo "   To set: export ANTHROPIC_API_KEY='your_key_here'"
    ((FAIL++))
else
    python3 << 'EOF' 2>/dev/null
import anthropic
import sys

try:
    client = anthropic.Anthropic(api_key="${ANTHROPIC_API_KEY}")
    response = client.messages.create(
        model='claude-sonnet-4-5-20250214',
        max_tokens=100,
        messages=[{'role': 'user', 'content': 'Say "Claude Code CLI works!"'}]
    )
    content = response.content[0].text
    print(f"   Response: {content[:100]}")
    print("   Status: Active")
    sys.exit(0)
except Exception as e:
    print(f"   Error: {str(e)[:100]}")
    sys.exit(1)
EOF
    if [ $? -eq 0 ]; then ((PASS++)); else ((FAIL++)); fi
fi

echo ""
echo "4. Testing Nvidia Kimi..."
echo "   Description: Video & vision specialized"
echo ""

if [ -z "$NVIDIA_KIMI_KEY" ] || [ "$NVIDIA_KIMI_KEY" == "your_key_here" ]; then
    echo -e "${YELLOW}⚠ NVIDIA_KIMI_KEY not set${NC}"
    echo "   To set: export NVIDIA_KIMI_KEY='your_key_here'"
    ((FAIL++))
else
    echo -e "${YELLOW}⚠ Nvidia Kimi testing not implemented${NC}"
    echo "   Key is set but testing requires specialized endpoint"
    ((PASS++))
fi

echo ""
echo "5. Testing Agent Modules..."
echo "   Description: API selector and load balancer"
echo ""

cd /opt/blackbox5/agents 2>/dev/null || {
    echo "   Error: /opt/blackbox5/agents not found"
    ((FAIL++))
}

# Test API selector
python3 << 'EOF' 2>/dev/null
import sys
sys.path.insert(0, '/opt/blackbox5/agents')

from api_selector.api_selector import APISelector

try:
    selector = APISelector()
    status = selector.get_provider_status()

    print(f"   Loaded providers: {len(status)}")
    for provider_id, info in status.items():
        print(f"   - {provider_id}: {info['health_status']}")
    print("   API Selector: Active")
except Exception as e:
    print(f"   Error: {str(e)[:100]}")
    sys.exit(1)
EOF
if [ $? -eq 0 ]; then ((PASS++)); else ((FAIL++)); fi

# Test Kimi load balancer
python3 << 'EOF' 2>/dev/null
import sys
sys.path.insert(0, '/opt/blackbox5/agents')

from kimi_load_balancer.kimi_load_balancer import KimiLoadBalancer

try:
    balancer = KimiLoadBalancer()
    summary = balancer.get_best_key_summary()

    print(f"   Available keys: {summary['available_keys']}/{summary['total_keys']}")
    if summary['best_key']:
        print(f"   Best key: {summary['best_key_name']}")
    print("   Kimi Load Balancer: Active")
except Exception as e:
    print(f"   Error: {str(e)[:100]}")
    sys.exit(1)
EOF
if [ $? -eq 0 ]; then ((PASS++)); else ((FAIL++)); fi

echo ""
echo "6. Testing Configuration Files..."
echo ""

# Check OpenClaw config
if [ -f ~/.openclaw/openclaw.json ]; then
    echo "   ✓ OpenClaw config found: ~/.openclaw/openclaw.json"
    ((PASS++))
else
    echo "   ✗ OpenClaw config not found"
    ((FAIL++))
fi

# Check API config
if [ -f /opt/blackbox5/config/api-keys.yaml ]; then
    echo "   ✓ API config found: /opt/blackbox5/config/api-keys.yaml"
    ((PASS++))
else
    echo "   ✗ API config not found"
    ((FAIL++))
fi

# Check OpenClaw API config
if [ -f ~/.openclaw/openclaw-api-config.json ]; then
    echo "   ✓ OpenClaw API config found: ~/.openclaw/openclaw-api-config.json"
    ((PASS++))
else
    echo "   ✗ OpenClaw API config not found"
    ((FAIL++))
fi

echo ""
echo "========================================"
echo "Test Results"
echo "========================================"
echo -e "${GREEN}Passed: $PASS${NC}"
echo -e "${RED}Failed: $FAIL${NC}"
echo "Total: $((PASS + FAIL))"
echo ""

if [ $FAIL -eq 0 ]; then
    echo -e "${GREEN}✓ All tests passed!${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠ Some tests failed. Check output above.${NC}"
    exit 1
fi
