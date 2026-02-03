"""
SISO-Relevant Scoring Weights v2

Ranks channels based on relevance to YOUR tech stack and current projects.
"""

# SISO Tech Stack Keywords (weighted by importance)
SISO_STACK = {
    # Critical - directly related to current work
    'critical': {
        'keywords': [
            'claude code', 'claude-code',
            'mcp', 'model context protocol',
            'anthropic',
        ],
        'weight': 3.0,
    },
    # High - AI engineering core
    'high': {
        'keywords': [
            'ai agent', 'ai agents', 'agentic',
            'vibe coding', 'vibe-coding',
            'cursor',
            'llm ops', 'llm-ops',
            'ai workflow', 'ai automation',
        ],
        'weight': 2.0,
    },
    # Medium - Related tech
    'medium': {
        'keywords': [
            'openai', 'gpt-4', 'gpt-5', 'chatgpt',
            'langchain', 'langgraph',
            'vector db', 'rag', 'embeddings',
            'prompt engineering',
            'context window', 'context management',
        ],
        'weight': 1.0,
    },
}

# Recency scoring (how recent is the tech being discussed)
RECENCY_KEYWORDS = {
    # 2025-2026 tech (highest score)
    'bleeding_edge': {
        'keywords': [
            'claude 3.5', 'claude 3.7', 'claude 4',
            'o3', 'o4', 'gpt-5',
            'deepseek v3', 'deepseek r1',
            'gemini 2.0', 'gemini 2.5',
            'mcp', 'model context protocol',
            'vibe coding',
            '2025', '2026',
        ],
        'score': 25,
    },
    # 2024 tech
    'current': {
        'keywords': [
            'claude 3', 'claude 3.0', 'claude 3 sonnet', 'claude 3 opus',
            'gpt-4o', 'gpt-4 turbo',
            'llama 3', 'llama 3.1',
            '2024',
        ],
        'score': 15,
    },
    # Older but relevant
    'established': {
        'keywords': [
            'gpt-4', 'gpt-3.5',
            'claude 2',
            'stable diffusion',
            'midjourney',
        ],
        'score': 5,
    },
}

# Actionability scoring (can you actually use this?)
ACTIONABILITY_INDICATORS = {
    'high': {
        'patterns': [
            'how to', 'tutorial', 'guide', 'walkthrough',
            'build', 'create', 'implement', 'setup',
            'step by step', 'step-by-step',
            'demo', 'live coding', 'coding session',
        ],
        'score': 20,
    },
    'medium': {
        'patterns': [
            'example', 'project', 'case study',
            'practical', 'hands-on',
            'code along', 'code-along',
        ],
        'score': 10,
    },
    'low': {
        'patterns': [
            'news', 'update', 'announced', 'released',
            'overview', 'introduction', 'explained',
            'what is', 'why', 'theory',
        ],
        'score': 2,
    },
}

# Content freshness (recency of upload)
FRESHNESS_SCORES = {
    'last_7_days': 30,
    'last_30_days': 20,
    'last_90_days': 10,
    'last_180_days': 5,
    'older': 0,
}

# New scoring weights (0-100 scale)
SCORING_DIMENSIONS = {
    'siso_relevance': 0.35,      # 35% - How relevant to YOUR stack
    'content_freshness': 0.25,   # 25% - How recent are the videos
    'tech_recency': 0.20,        # 20% - How current is the tech discussed
    'actionability': 0.15,       # 15% - Can you actually use this?
    'consistency': 0.05,         # 5% - Upload consistency (bonus)
}

# Tier thresholds
TIER_THRESHOLDS = {
    'S': (85, 100),   # Must watch - directly applicable
    'A': (70, 84),    # Excellent - highly relevant
    'B': (55, 69),    # Good - worth checking
    'C': (40, 54),    # Average - occasional value
    'D': (0, 39),     # Low - not relevant to current stack
}


def get_siso_stack_matches(text):
    """Find SISO stack keyword matches in text."""
    text_lower = text.lower()
    matches = []
    total_weight = 0

    for priority, data in SISO_STACK.items():
        for keyword in data['keywords']:
            if keyword in text_lower:
                matches.append({
                    'keyword': keyword,
                    'priority': priority,
                    'weight': data['weight'],
                })
                total_weight += data['weight']

    return matches, total_weight


def get_recency_score(text):
    """Score based on how recent/current the tech is."""
    text_lower = text.lower()
    score = 0
    matches = []

    for category, data in RECENCY_KEYWORDS.items():
        for keyword in data['keywords']:
            if keyword in text_lower:
                score += data['score']
                matches.append(keyword)

    # Cap at 100
    return min(score, 100), matches


def get_actionability_score(text):
    """Score based on how actionable the content is."""
    text_lower = text.lower()
    score = 0
    matches = []

    for level, data in ACTIONABILITY_INDICATORS.items():
        for pattern in data['patterns']:
            if pattern in text_lower:
                score += data['score']
                matches.append(pattern)
                break  # Only count once per level

    # Cap at 100
    return min(score, 100), matches


def get_freshness_score(upload_date_str):
    """Score based on how recent the video is."""
    from datetime import datetime, timedelta

    if not upload_date_str:
        return 0

    try:
        upload_date = datetime.strptime(upload_date_str, '%Y%m%d')
        days_ago = (datetime.now() - upload_date).days

        if days_ago <= 7:
            return FRESHNESS_SCORES['last_7_days']
        elif days_ago <= 30:
            return FRESHNESS_SCORES['last_30_days']
        elif days_ago <= 90:
            return FRESHNESS_SCORES['last_90_days']
        elif days_ago <= 180:
            return FRESHNESS_SCORES['last_180_days']
        else:
            return FRESHNESS_SCORES['older']
    except:
        return 0


def get_tier(score):
    """Determine tier based on SISO-relevant score."""
    for tier, (min_score, max_score) in TIER_THRESHOLDS.items():
        if min_score <= score <= max_score:
            return tier
    return 'D'
