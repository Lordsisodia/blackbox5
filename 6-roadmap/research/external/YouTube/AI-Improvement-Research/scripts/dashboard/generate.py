#!/usr/bin/env python3
"""
Generate HTML Dashboard for YouTube Channel Rankings

Creates an interactive static HTML dashboard with:
- Sortable leaderboard table
- Category filtering
- Channel detail cards
- Tier distribution charts
- Trending indicators
"""

import json
from pathlib import Path
from datetime import datetime
from string import Template


HTML_TEMPLATE = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Channel Leaderboard - AI/ML Education</title>
    <style>
        :root {
            --bg-primary: #0d1117;
            --bg-secondary: #161b22;
            --bg-tertiary: #21262d;
            --text-primary: #e6edf3;
            --text-secondary: #8b949e;
            --border-color: #30363d;
            --accent-blue: #58a6ff;
            --accent-green: #238636;
            --accent-yellow: #d29922;
            --accent-red: #da3633;
            --accent-purple: #8957e5;
            --tier-s: #ffd700;
            --tier-a: #00ff88;
            --tier-b: #58a6ff;
            --tier-c: #8b949e;
            --tier-d: #da3633;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
        }

        .container {
            max-width: 1400px;
            margin: 0 auto;
            padding: 20px;
        }

        header {
            text-align: center;
            padding: 40px 0;
            border-bottom: 1px solid var(--border-color);
            margin-bottom: 30px;
        }

        h1 {
            font-size: 2.5rem;
            margin-bottom: 10px;
            background: linear-gradient(90deg, var(--accent-blue), var(--accent-purple));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: var(--text-secondary);
            font-size: 1.1rem;
        }

        .meta {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 10px;
        }

        /* Stats Grid */
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        }

        .stat-value {
            font-size: 2rem;
            font-weight: bold;
            color: var(--accent-blue);
        }

        .stat-label {
            color: var(--text-secondary);
            font-size: 0.9rem;
            margin-top: 5px;
        }

        /* Tier Distribution */
        .tier-distribution {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .tier-bar {
            display: flex;
            height: 40px;
            border-radius: 8px;
            overflow: hidden;
            margin-top: 15px;
        }

        .tier-segment {
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 0.9rem;
            transition: opacity 0.2s;
        }

        .tier-segment:hover {
            opacity: 0.8;
        }

        /* Filters */
        .filters {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            display: flex;
            flex-wrap: wrap;
            gap: 15px;
            align-items: center;
        }

        .filter-group {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        label {
            color: var(--text-secondary);
            font-size: 0.9rem;
        }

        select, input {
            background: var(--bg-tertiary);
            border: 1px solid var(--border-color);
            color: var(--text-primary);
            padding: 8px 12px;
            border-radius: 6px;
            font-size: 0.9rem;
        }

        /* Table */
        .table-container {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
        }

        table {
            width: 100%;
            border-collapse: collapse;
        }

        th {
            background: var(--bg-tertiary);
            padding: 15px;
            text-align: left;
            font-weight: 600;
            color: var(--text-secondary);
            cursor: pointer;
            user-select: none;
            transition: background 0.2s;
        }

        th:hover {
            background: var(--border-color);
        }

        th.sortable::after {
            content: ' ↕';
            opacity: 0.5;
        }

        th.sort-asc::after {
            content: ' ↑';
            opacity: 1;
        }

        th.sort-desc::after {
            content: ' ↓';
            opacity: 1;
        }

        td {
            padding: 15px;
            border-top: 1px solid var(--border-color);
        }

        tr:hover {
            background: var(--bg-tertiary);
        }

        /* Tier Badges */
        .tier-badge {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 4px;
            font-weight: bold;
            font-size: 0.85rem;
        }

        .tier-s { background: rgba(255, 215, 0, 0.2); color: var(--tier-s); }
        .tier-a { background: rgba(0, 255, 136, 0.2); color: var(--tier-a); }
        .tier-b { background: rgba(88, 166, 255, 0.2); color: var(--tier-b); }
        .tier-c { background: rgba(139, 148, 158, 0.2); color: var(--tier-c); }
        .tier-d { background: rgba(218, 54, 51, 0.2); color: var(--tier-d); }

        /* Score Bars */
        .score-bar {
            width: 100%;
            height: 6px;
            background: var(--bg-tertiary);
            border-radius: 3px;
            overflow: hidden;
            margin-top: 5px;
        }

        .score-fill {
            height: 100%;
            border-radius: 3px;
            transition: width 0.3s;
        }

        .score-fill.high { background: var(--accent-green); }
        .score-fill.medium { background: var(--accent-yellow); }
        .score-fill.low { background: var(--accent-red); }

        /* Trend Indicators */
        .trend {
            font-size: 1.2rem;
        }

        .trend-rising { color: var(--accent-green); }
        .trend-falling { color: var(--accent-red); }
        .trend-stable { color: var(--text-secondary); }
        .trend-new { color: var(--accent-purple); }

        /* Channel Link */
        .channel-name {
            color: var(--accent-blue);
            text-decoration: none;
            font-weight: 500;
        }

        .channel-name:hover {
            text-decoration: underline;
        }

        /* Component Scores */
        .component-scores {
            display: flex;
            gap: 8px;
            font-size: 0.8rem;
        }

        .component-score {
            padding: 2px 6px;
            background: var(--bg-tertiary);
            border-radius: 4px;
            color: var(--text-secondary);
        }

        /* Responsive */
        @media (max-width: 768px) {
            h1 { font-size: 1.8rem; }
            .stats-grid { grid-template-columns: repeat(2, 1fr); }
            .filters { flex-direction: column; align-items: stretch; }
            th, td { padding: 10px; font-size: 0.85rem; }
            .component-scores { flex-wrap: wrap; }
        }

        /* Footer */
        footer {
            text-align: center;
            padding: 40px 0;
            color: var(--text-secondary);
            font-size: 0.9rem;
            border-top: 1px solid var(--border-color);
            margin-top: 40px;
        }

        .methodology {
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 30px;
        }

        .methodology h2 {
            margin-bottom: 15px;
            color: var(--text-primary);
        }

        .methodology ul {
            list-style: none;
            padding-left: 0;
        }

        .methodology li {
            padding: 8px 0;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            justify-content: space-between;
        }

        .methodology li:last-child {
            border-bottom: none;
        }

        .weight {
            color: var(--accent-blue);
            font-weight: 500;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏆 YouTube Channel Leaderboard</h1>
            <p class="subtitle">AI/ML & Programming Education Rankings</p>
            <p class="meta">Generated: ${generated_at} | ${total_channels} channels ranked</p>
        </header>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">${total_channels}</div>
                <div class="stat-label">Total Channels</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--tier-s)">${tier_s_count}</div>
                <div class="stat-label">S-Tier Channels</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--tier-a)">${tier_a_count}</div>
                <div class="stat-label">A-Tier Channels</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" style="color: var(--accent-blue)">${top_score}</div>
                <div class="stat-label">Top Score</div>
            </div>
        </div>

        <div class="tier-distribution">
            <h3>Tier Distribution</h3>
            <div class="tier-bar">
                ${tier_bar}
            </div>
        </div>

        <div class="methodology">
            <h2>📊 Scoring Methodology</h2>
            <ul>
                <li>Knowledge Density <span class="weight">25%</span></li>
                <li>Engagement Quality <span class="weight">20%</span></li>
                <li>Consistency <span class="weight">20%</span></li>
                <li>Production Quality <span class="weight">15%</span></li>
                <li>Long-term Impact <span class="weight">15%</span></li>
                <li>Content Novelty <span class="weight">5%</span></li>
            </ul>
        </div>

        <div class="filters">
            <div class="filter-group">
                <label for="category-filter">Category:</label>
                <select id="category-filter">
                    <option value="all">All Categories</option>
                    ${category_options}
                </select>
            </div>
            <div class="filter-group">
                <label for="tier-filter">Tier:</label>
                <select id="tier-filter">
                    <option value="all">All Tiers</option>
                    <option value="S">S-Tier</option>
                    <option value="A">A-Tier</option>
                    <option value="B">B-Tier</option>
                    <option value="C">C-Tier</option>
                    <option value="D">D-Tier</option>
                </select>
            </div>
            <div class="filter-group">
                <label for="search">Search:</label>
                <input type="text" id="search" placeholder="Channel name...">
            </div>
        </div>

        <div class="table-container">
            <table id="leaderboard">
                <thead>
                    <tr>
                        <th class="sortable" data-column="rank">Rank</th>
                        <th class="sortable" data-column="tier">Tier</th>
                        <th>Channel</th>
                        <th class="sortable" data-column="score">Score</th>
                        <th>Trend</th>
                        <th>Components</th>
                    </tr>
                </thead>
                <tbody>
                    ${table_rows}
                </tbody>
            </table>
        </div>

        <footer>
            <p>Rankings update daily at 6 AM UTC</p>
            <p style="margin-top: 10px; font-size: 0.8rem;">
                Scores are calculated based on educational value metrics derived from publicly available video metadata.
            </p>
        </footer>
    </div>

    <script>
        // Sorting functionality
        document.querySelectorAll('th.sortable').forEach(th => {
            th.addEventListener('click', () => {
                const column = th.dataset.column;
                const isAsc = th.classList.contains('sort-asc');

                // Reset all headers
                document.querySelectorAll('th').forEach(h => {
                    h.classList.remove('sort-asc', 'sort-desc');
                });

                // Set new sort direction
                th.classList.add(isAsc ? 'sort-desc' : 'sort-asc');

                sortTable(column, !isAsc);
            });
        });

        function sortTable(column, asc) {
            const tbody = document.querySelector('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));

            rows.sort((a, b) => {
                let aVal, bVal;

                if (column === 'rank') {
                    aVal = parseInt(a.cells[0].textContent);
                    bVal = parseInt(b.cells[0].textContent);
                } else if (column === 'tier') {
                    const tierOrder = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1};
                    aVal = tierOrder[a.cells[1].textContent.trim()] || 0;
                    bVal = tierOrder[b.cells[1].textContent.trim()] || 0;
                } else if (column === 'score') {
                    aVal = parseFloat(a.cells[3].textContent);
                    bVal = parseFloat(b.cells[3].textContent);
                }

                return asc ? aVal - bVal : bVal - aVal;
            });

            rows.forEach(row => tbody.appendChild(row));
        }

        // Filtering functionality
        const categoryFilter = document.getElementById('category-filter');
        const tierFilter = document.getElementById('tier-filter');
        const searchInput = document.getElementById('search');

        function filterTable() {
            const category = categoryFilter.value;
            const tier = tierFilter.value;
            const search = searchInput.value.toLowerCase();

            document.querySelectorAll('tbody tr').forEach(row => {
                const rowCategory = row.dataset.category;
                const rowTier = row.cells[1].textContent.trim();
                const rowName = row.cells[2].textContent.toLowerCase();

                const categoryMatch = category === 'all' || rowCategory === category;
                const tierMatch = tier === 'all' || rowTier === tier;
                const searchMatch = rowName.includes(search);

                row.style.display = categoryMatch && tierMatch && searchMatch ? '' : 'none';
            });
        }

        categoryFilter.addEventListener('change', filterTable);
        tierFilter.addEventListener('change', filterTable);
        searchInput.addEventListener('input', filterTable);
    </script>
</body>
</html>'''


def generate_tier_bar(tier_counts, total):
    """Generate HTML for tier distribution bar."""
    colors = {
        'S': '#ffd700',
        'A': '#00ff88',
        'B': '#58a6ff',
        'C': '#8b949e',
        'D': '#da3633'
    }

    segments = []
    for tier in ['S', 'A', 'B', 'C', 'D']:
        count = tier_counts.get(tier, 0)
        if count > 0:
            pct = (count / total) * 100
            segments.append(
                f'<div class="tier-segment" style="width: {pct}%; background: {colors[tier]}20; color: {colors[tier]};">'
                f'{tier}</div>'
            )

    return ''.join(segments)


def generate_category_options(categories):
    """Generate category filter options."""
    options = []
    for key, name in categories.items():
        options.append(f'<option value="{key}">{name}</option>')
    return '\n'.join(options)


def generate_table_rows(rankings):
    """Generate HTML table rows."""
    rows = []

    for i, channel in enumerate(rankings['overall'], 1):
        tier = channel['tier']
        trend = channel.get('trend', 'stable')
        trend_icons = {
            'rising': '↑',
            'falling': '↓',
            'stable': '→',
            'new': '✨'
        }
        trend_icon = trend_icons.get(trend, '→')

        components = channel['component_scores']
        component_html = (
            f'<span class="component-score" title="Knowledge">K:{components["knowledge"]:.0f}</span>'
            f'<span class="component-score" title="Engagement">E:{components["engagement"]:.0f}</span>'
            f'<span class="component-score" title="Consistency">C:{components["consistency"]:.0f}</span>'
        )

        categories = channel.get('categories', [])
        primary_category = categories[0] if categories else 'programming'

        score_class = 'high' if channel['overall_score'] >= 80 else 'medium' if channel['overall_score'] >= 60 else 'low'

        rows.append(f'''
            <tr data-category="{primary_category}">
                <td>#{i}</td>
                <td><span class="tier-badge tier-{tier.lower()}">{tier}</span></td>
                <td><span class="channel-name">{channel["channel_name"]}</span></td>
                <td>
                    <strong>{channel["overall_score"]:.1f}</strong>
                    <div class="score-bar">
                        <div class="score-fill {score_class}" style="width: {channel["overall_score"]}%"></div>
                    </div>
                </td>
                <td><span class="trend trend-{trend}">{trend_icon}</span></td>
                <td><div class="component-scores">{component_html}</div></td>
            </tr>
        ''')

    return '\n'.join(rows)


def generate_dashboard(rankings_path, output_path):
    """Generate HTML dashboard from rankings JSON."""
    with open(rankings_path, 'r') as f:
        rankings = json.load(f)

    # Calculate stats
    total = rankings['total_channels']
    tiers = [ch['tier'] for ch in rankings['overall']]
    tier_counts = {t: tiers.count(t) for t in set(tiers)}
    top_score = rankings['overall'][0]['overall_score'] if rankings['overall'] else 0

    # Category names
    categories = {
        'data_science': 'Data Science',
        'machine_learning': 'Machine Learning / AI',
        'programming': 'Programming',
        'web_development': 'Web Development',
        'ai_research': 'AI Research',
        'devops': 'DevOps',
        'career': 'Career / Business',
        'mobile': 'Mobile Development',
        'cybersecurity': 'Cybersecurity'
    }

    # Use string.Template for safe substitution
    template = Template(HTML_TEMPLATE)
    html = template.substitute(
        generated_at=datetime.now().strftime('%Y-%m-%d %H:%M UTC'),
        total_channels=total,
        tier_s_count=tier_counts.get('S', 0),
        tier_a_count=tier_counts.get('A', 0),
        top_score=f"{top_score:.1f}",
        tier_bar=generate_tier_bar(tier_counts, total),
        category_options=generate_category_options(categories),
        table_rows=generate_table_rows(rankings)
    )

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)

    print(f"Dashboard generated: {output_path}")


def main():
    """Main entry point."""
    base_dir = Path(__file__).parent.parent.parent
    rankings_path = base_dir / 'database' / 'channel_rankings.json'
    output_path = base_dir / 'dashboard' / 'index.html'

    if not rankings_path.exists():
        print(f"Rankings file not found: {rankings_path}")
        print("Run generate_rankings.py first.")
        return

    generate_dashboard(rankings_path, output_path)


if __name__ == '__main__':
    main()
