"""
Channel Category Classification

Assigns channels to categories based on their content focus.
"""

from typing import Dict, List, Optional
from pathlib import Path
import json

# Category definitions with keywords for classification
CATEGORY_DEFINITIONS = {
    'data_science': {
        'name': 'Data Science / Data Analysis',
        'keywords': [
            'data science', 'data analysis', 'pandas', 'numpy', 'data visualization',
            'matplotlib', 'seaborn', 'tableau', 'power bi', 'sql', 'database',
            'jupyter', 'notebook', 'csv', 'dataframe', 'eda', 'exploratory',
            'data cleaning', 'data preprocessing', 'feature engineering',
            'ken jee', 'tina huang', 'data professor', 'krish naik', 'alex analyst',
            'luke barousse', 'import data', 'dataslice'
        ],
    },
    'machine_learning': {
        'name': 'Machine Learning / AI',
        'keywords': [
            'machine learning', 'deep learning', 'neural network', 'ai', 'artificial intelligence',
            'tensorflow', 'pytorch', 'keras', 'scikit-learn', 'sklearn', 'ml',
            'model training', 'supervised learning', 'unsupervised learning',
            'reinforcement learning', 'computer vision', 'nlp', 'natural language',
            'transformer', 'bert', 'gpt', 'llm', 'large language model',
            'yannic kilcher', 'sentdex', 'deeplizard', 'codeemporium', 'ai coffee',
            'whats ai', 'ai explained', 'ai revolution', 'ai advantage', 'ai jason'
        ],
    },
    'programming': {
        'name': 'Programming / Software Engineering',
        'keywords': [
            'programming', 'coding', 'software engineering', 'algorithm', 'data structure',
            'leetcode', 'interview', 'system design', 'clean code', 'refactoring',
            'design pattern', 'oop', 'object oriented', 'functional programming',
            'debugging', 'testing', 'tdd', 'ci/cd', 'devops', 'git', 'github',
            'freecodecamp', 'fireship', 'cs dojo', 'tech with tim', 'programming with mosh',
            'the coding train', 'mCoding', 'back to back swe', 'william lin', 'errichto'
        ],
    },
    'web_development': {
        'name': 'Web Development',
        'keywords': [
            'web development', 'web dev', 'html', 'css', 'javascript', 'js',
            'react', 'vue', 'angular', 'svelte', 'frontend', 'backend', 'full stack',
            'node.js', 'nodejs', 'express', 'django', 'flask', 'fastapi',
            'next.js', 'nuxt', 'tailwind', 'bootstrap', 'sass', 'less',
            'traversy media', 'net ninja', 'dev ed', 'kevin powell', 'florin pop',
            'javascript mastery', 'web dev simplified', 'fireship'
        ],
    },
    'ai_research': {
        'name': 'AI Research',
        'keywords': [
            'ai research', 'machine learning research', 'deep learning research',
            'paper review', 'arxiv', 'research paper', 'state of the art',
            'sota', 'benchmark', 'dataset', 'model architecture',
            'yannic kilcher', 'two minute papers', 'ai journal', 'arxiv insights',
            'bycloud', 'machine learning street talk', 'andrej karpathy',
            'deepmind', 'openai', 'anthropic', 'google research'
        ],
    },
    'devops': {
        'name': 'DevOps / Infrastructure',
        'keywords': [
            'devops', 'docker', 'kubernetes', 'k8s', 'cloud', 'aws', 'azure', 'gcp',
            'terraform', 'ansible', 'jenkins', 'github actions', 'cicd',
            'linux', 'server', 'infrastructure', 'deployment', 'monitoring',
            'networkchuck', 'techworld with nana', 'seattle data guy'
        ],
    },
    'career': {
        'name': 'Career / Business',
        'keywords': [
            'career', 'job search', 'interview prep', 'salary', 'negotiation',
            'freelance', 'startup', 'entrepreneurship', 'side project',
            'portfolio', 'resume', 'linkedin', 'networking',
            'joma tech', 'mayuko', 'forrest knight', 'clément mihailescu'
        ],
    },
    'mobile': {
        'name': 'Mobile Development',
        'keywords': [
            'mobile development', 'android', 'ios', 'swift', 'kotlin',
            'react native', 'flutter', 'dart', 'mobile app', 'app development',
            'flutter way', 'tadas petra', 'robert brunhage'
        ],
    },
    'python': {
        'name': 'Python',
        'keywords': [
            'python', 'python tutorial', 'python programming', 'pandas', 'numpy',
            'corey schafer', 'sentdex', 'real python', 'neuralnine', 'mCoding'
        ],
    },
    'cybersecurity': {
        'name': 'Cybersecurity',
        'keywords': [
            'cybersecurity', 'security', 'hacking', 'penetration testing',
            'network security', 'cyber', 'infosec', 'networkchuck'
        ],
    },
}


def categorize_channel(channel_name: str, video_titles: Optional[List[str]] = None) -> List[str]:
    """
    Assign channel to categories based on name and video titles.

    Args:
        channel_name: Name of the channel
        video_titles: Optional list of recent video titles

    Returns:
        List of category keys
    """
    scores = {cat: 0 for cat in CATEGORY_DEFINITIONS}

    # Score based on channel name
    name_lower = channel_name.lower()
    for cat_key, cat_def in CATEGORY_DEFINITIONS.items():
        for keyword in cat_def['keywords']:
            if keyword.lower() in name_lower:
                scores[cat_key] += 3  # Higher weight for name match

    # Score based on video titles
    if video_titles:
        for title in video_titles:
            title_lower = title.lower()
            for cat_key, cat_def in CATEGORY_DEFINITIONS.items():
                for keyword in cat_def['keywords']:
                    if keyword.lower() in title_lower:
                        scores[cat_key] += 1

    # Return categories with scores above threshold
    threshold = 2
    matches = [cat for cat, score in scores.items() if score >= threshold]

    # If no matches, default to 'programming'
    if not matches:
        matches = ['programming']

    return matches


def get_category_name(category_key: str) -> str:
    """Get human-readable category name."""
    if category_key in CATEGORY_DEFINITIONS:
        return CATEGORY_DEFINITIONS[category_key]['name']
    return category_key.replace('_', ' ').title()


def get_category_channels(channel_scores: Dict, category: str) -> List[Dict]:
    """
    Get all channels belonging to a specific category.

    Args:
        channel_scores: Dictionary of channel score results
        category: Category key

    Returns:
        List of channel score dictionaries
    """
    matching = []
    for channel_id, score_data in channel_scores.items():
        categories = score_data.get('categories', [])
        if category in categories:
            matching.append(score_data)

    # Sort by overall score
    matching.sort(key=lambda x: x['overall_score'], reverse=True)
    return matching


def generate_category_rankings(channel_scores: Dict) -> Dict[str, List[Dict]]:
    """
    Generate rankings for all categories.

    Args:
        channel_scores: Dictionary of channel score results

    Returns:
        Dictionary mapping category to ranked list
    """
    rankings = {}
    for cat_key in CATEGORY_DEFINITIONS:
        rankings[cat_key] = get_category_channels(channel_scores, cat_key)
    return rankings


if __name__ == '__main__':
    # Test categorization
    test_channels = [
        ('Fireship', ['JavaScript in 100 Seconds', 'React Tutorial']),
        ('Ken Jee', ['Data Science Roadmap 2024']),
        ('Yannic Kilcher', ['Paper Explained: GPT-4']),
        ('Traversy Media', ['React Crash Course']),
    ]

    for name, titles in test_channels:
        cats = categorize_channel(name, titles)
        print(f"{name}: {[get_category_name(c) for c in cats]}")
