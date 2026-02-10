/**
 * BlackBox5 Autonomous Improvement Dashboard Widget
 * Displays real-time improvement cycle status, metrics, and agent utilization
 */

class AutonomousImprovementDashboard {
    constructor() {
        this.bb5Home = '/opt/blackbox5';
        this.autonomousDir = `${this.bb5Home}/.autonomous`;
        this.metricsFile = `${this.autonomousDir}/metrics/latest-cycle.json`;
        this.logFile = `${this.autonomousDir}/improvement-log.md`;
        this.planFile = `${this.autonomousDir}/improvement-plan.yaml`;

        this.currentMetrics = null;
        this.refreshInterval = 30000; // 30 seconds
        this.refreshTimer = null;

        this.init();
    }

    init() {
        console.log('🚀 Initializing Autonomous Improvement Dashboard...');

        // Create dashboard widget container
        this.createWidgetContainer();

        // Load initial data
        this.refreshData();

        // Start auto-refresh
        this.startAutoRefresh();

        console.log('✅ Autonomous Improvement Dashboard initialized');
    }

    createWidgetContainer() {
        // Check if container already exists
        if (document.getElementById('autonomous-improvement-widget')) {
            return;
        }

        // Create widget HTML
        const widgetHtml = `
            <div id="autonomous-improvement-widget" class="dashboard-widget">
                <div class="widget-header">
                    <h2>🤖 Autonomous Improvement</h2>
                    <div class="widget-actions">
                        <button id="refresh-btn" class="btn btn-sm">🔄 Refresh</button>
                        <button id="view-log-btn" class="btn btn-sm">📄 View Log</button>
                    </div>
                </div>

                <div class="widget-content">
                    <!-- Status Section -->
                    <div class="section status-section">
                        <h3>Current Cycle Status</h3>
                        <div id="cycle-status" class="status-display">
                            <div class="status-indicator" data-status="loading">
                                <span class="indicator"></span>
                                <span class="status-text">Loading...</span>
                            </div>
                        </div>
                    </div>

                    <!-- Metrics Section -->
                    <div class="section metrics-section">
                        <h3>📊 Improvement Metrics</h3>
                        <div class="metrics-grid">
                            <div class="metric-card">
                                <div class="metric-value" id="tasks-analyzed">-</div>
                                <div class="metric-label">Tasks Analyzed</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value" id="tasks-completed">-</div>
                                <div class="metric-label">Tasks Completed</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value" id="agents-used">-</div>
                                <div class="metric-label">Agents Used</div>
                            </div>
                            <div class="metric-card">
                                <div class="metric-value" id="success-rate">-</div>
                                <div class="metric-label">Success Rate</div>
                            </div>
                        </div>
                    </div>

                    <!-- Agent Utilization Section -->
                    <div class="section agents-section">
                        <h3>👥 Agent Utilization</h3>
                        <div id="agent-utilization" class="agent-grid">
                            <div class="loading">Loading agent data...</div>
                        </div>
                    </div>

                    <!-- Recent Cycles Section -->
                    <div class="section cycles-section">
                        <h3>📈 Recent Improvement Cycles</h3>
                        <div id="recent-cycles" class="cycles-list">
                            <div class="loading">Loading cycle history...</div>
                        </div>
                    </div>

                    <!-- Active Tasks Section -->
                    <div class="section tasks-section">
                        <h3>🎯 Top Priority Tasks</h3>
                        <div id="active-tasks" class="tasks-list">
                            <div class="loading">Loading tasks...</div>
                        </div>
                    </div>
                </div>
            </div>
        `;

        // Insert into dashboard
        document.body.insertAdjacentHTML('beforeend', widgetHtml);

        // Add event listeners
        document.getElementById('refresh-btn').addEventListener('click', () => this.refreshData());
        document.getElementById('view-log-btn').addEventListener('click', () => this.viewLog());

        // Add CSS styles
        this.addStyles();
    }

    addStyles() {
        const styleId = 'autonomous-improvement-styles';
        if (document.getElementById(styleId)) {
            return;
        }

        const css = `
            <style id="${styleId}">
                #autonomous-improvement-widget {
                    background: #1a1a2e;
                    border: 1px solid #4a4a6a;
                    border-radius: 12px;
                    padding: 20px;
                    margin: 20px 0;
                    color: #e0e0e0;
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                }

                #autonomous-improvement-widget .widget-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    margin-bottom: 20px;
                    padding-bottom: 15px;
                    border-bottom: 1px solid #4a4a6a;
                }

                #autonomous-improvement-widget h2 {
                    margin: 0;
                    font-size: 24px;
                    color: #00ff88;
                }

                #autonomous-improvement-widget .widget-actions {
                    display: flex;
                    gap: 10px;
                }

                #autonomous-improvement-widget .btn {
                    background: #4a4a6a;
                    border: none;
                    color: #fff;
                    padding: 8px 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    font-size: 14px;
                    transition: background 0.2s;
                }

                #autonomous-improvement-widget .btn:hover {
                    background: #5a5a7a;
                }

                #autonomous-improvement-widget .section {
                    margin: 20px 0;
                    padding: 15px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 8px;
                }

                #autonomous-improvement-widget h3 {
                    margin: 0 0 15px 0;
                    font-size: 18px;
                    color: #00ff88;
                }

                #autonomous-improvement-widget .status-indicator {
                    display: flex;
                    align-items: center;
                    gap: 10px;
                    padding: 15px;
                    background: rgba(0, 255, 136, 0.1);
                    border-radius: 8px;
                    border-left: 4px solid #00ff88;
                }

                #autonomous-improvement-widget .status-indicator[data-status="running"] {
                    border-left-color: #ffaa00;
                    background: rgba(255, 170, 0, 0.1);
                }

                #autonomous-improvement-widget .status-indicator[data-status="idle"] {
                    border-left-color: #00aaff;
                    background: rgba(0, 170, 255, 0.1);
                }

                #autonomous-improvement-widget .indicator {
                    width: 12px;
                    height: 12px;
                    border-radius: 50%;
                    background: #00ff88;
                    animation: pulse 2s infinite;
                }

                @keyframes pulse {
                    0%, 100% { opacity: 1; }
                    50% { opacity: 0.5; }
                }

                #autonomous-improvement-widget .metrics-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
                    gap: 15px;
                }

                #autonomous-improvement-widget .metric-card {
                    background: rgba(255, 255, 255, 0.05);
                    padding: 15px;
                    border-radius: 8px;
                    text-align: center;
                }

                #autonomous-improvement-widget .metric-value {
                    font-size: 32px;
                    font-weight: bold;
                    color: #00ff88;
                    margin-bottom: 5px;
                }

                #autonomous-improvement-widget .metric-label {
                    font-size: 14px;
                    color: #a0a0a0;
                }

                #autonomous-improvement-widget .agent-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                    gap: 10px;
                }

                #autonomous-improvement-widget .agent-card {
                    background: rgba(255, 255, 255, 0.05);
                    padding: 10px;
                    border-radius: 6px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }

                #autonomous-improvement-widget .agent-icon {
                    font-size: 24px;
                }

                #autonomous-improvement-widget .agent-name {
                    font-weight: bold;
                    font-size: 14px;
                }

                #autonomous-improvement-widget .agent-tasks {
                    font-size: 12px;
                    color: #a0a0a0;
                }

                #autonomous-improvement-widget .tasks-list,
                #autonomous-improvement-widget .cycles-list {
                    max-height: 300px;
                    overflow-y: auto;
                }

                #autonomous-improvement-widget .task-item,
                #autonomous-improvement-widget .cycle-item {
                    padding: 10px;
                    background: rgba(255, 255, 255, 0.05);
                    border-radius: 6px;
                    margin-bottom: 8px;
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                }

                #autonomous-improvement-widget .task-name {
                    font-weight: bold;
                }

                #autonomous-improvement-widget .task-meta {
                    font-size: 12px;
                    color: #a0a0a0;
                }

                #autonomous-improvement-widget .priority-high {
                    color: #ff4444;
                }

                #autonomous-improvement-widget .priority-medium {
                    color: #ffaa00;
                }

                #autonomous-improvement-widget .priority-low {
                    color: #00aaff;
                }

                #autonomous-improvement-widget .loading {
                    text-align: center;
                    color: #a0a0a0;
                    padding: 20px;
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', css);
    }

    async refreshData() {
        console.log('🔄 Refreshing dashboard data...');

        try {
            // Load metrics
            await this.loadMetrics();

            // Update UI
            this.updateUI();

            console.log('✅ Dashboard data refreshed');
        } catch (error) {
            console.error('❌ Failed to refresh dashboard data:', error);
            this.showError('Failed to load data');
        }
    }

    async loadMetrics() {
        try {
            const response = await fetch(`/api/metrics/autonomous-improvement`);
            if (response.ok) {
                this.currentMetrics = await response.json();
            } else {
                console.warn('Metrics endpoint not available, using default values');
                this.currentMetrics = this.getDefaultMetrics();
            }
        } catch (error) {
            console.warn('Could not load metrics, using defaults:', error);
            this.currentMetrics = this.getDefaultMetrics();
        }
    }

    getDefaultMetrics() {
        return {
            timestamp: new Date().toISOString(),
            tasks_analyzed: 0,
            tasks_completed: 0,
            agents_used: 0,
            success_rate: 0,
            agent_reports: [],
            status: 'idle'
        };
    }

    updateUI() {
        const metrics = this.currentMetrics;

        // Update status
        this.updateStatus(metrics.status || 'idle');

        // Update metrics
        document.getElementById('tasks-analyzed').textContent = metrics.tasks_analyzed || 0;
        document.getElementById('tasks-completed').textContent = metrics.tasks_completed || 0;
        document.getElementById('agents-used').textContent = metrics.agents_used || 0;
        document.getElementById('success-rate').textContent =
            (metrics.success_rate || 0).toFixed(1) + '%';

        // Update agent utilization
        this.updateAgentUtilization(metrics.agent_reports || []);

        // Update recent cycles (placeholder)
        this.updateRecentCycles([]);

        // Update active tasks (placeholder)
        this.updateActiveTasks([]);
    }

    updateStatus(status) {
        const statusIndicator = document.querySelector('.status-indicator');
        if (!statusIndicator) return;

        statusIndicator.setAttribute('data-status', status);

        const statusText = statusIndicator.querySelector('.status-text');
        const statusMessages = {
            running: '🔄 Improvement cycle running...',
            idle: '✅ Waiting for next cycle',
            loading: '⏳ Loading...'
        };
        statusText.textContent = statusMessages[status] || status;
    }

    updateAgentUtilization(agentReports) {
        const container = document.getElementById('agent-utilization');
        if (!container) return;

        if (!agentReports || agentReports.length === 0) {
            container.innerHTML = '<div class="loading">No agent activity yet</div>';
            return;
        }

        // Count tasks per agent
        const agentCounts = {};
        agentReports.forEach(report => {
            const agentId = report.agent || 'unknown';
            agentCounts[agentId] = (agentCounts[agentId] || 0) + 1;
        });

        // Generate agent cards
        const agentIcons = {
            architect: '🏗️',
            engineering: '🔧',
            'engineering-senior': '⚙️',
            testing: '🧪',
            verification: '✅',
            scribe: '📝'
        };

        let html = '';
        for (const [agentId, count] of Object.entries(agentCounts)) {
            const icon = agentIcons[agentId] || '🤖';
            html += `
                <div class="agent-card">
                    <span class="agent-icon">${icon}</span>
                    <div>
                        <div class="agent-name">${agentId}</div>
                        <div class="agent-tasks">${count} task(s)</div>
                    </div>
                </div>
            `;
        }

        container.innerHTML = html;
    }

    updateRecentCycles(cycles) {
        const container = document.getElementById('recent-cycles');
        if (!container) return;

        if (!cycles || cycles.length === 0) {
            container.innerHTML = '<div class="loading">No cycles completed yet</div>';
            return;
        }

        let html = '';
        cycles.forEach(cycle => {
            html += `
                <div class="cycle-item">
                    <div>
                        <div class="task-name">Cycle: ${cycle.cycle_id}</div>
                        <div class="task-meta">${cycle.timestamp}</div>
                    </div>
                    <div class="priority-medium">${cycle.tasks_completed} tasks</div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    updateActiveTasks(tasks) {
        const container = document.getElementById('active-tasks');
        if (!container) return;

        if (!tasks || tasks.length === 0) {
            container.innerHTML = '<div class="loading">No active tasks</div>';
            return;
        }

        let html = '';
        tasks.slice(0, 5).forEach(task => {
            const priorityClass = `priority-${task.priority || 'medium'}`;
            html += `
                <div class="task-item">
                    <div>
                        <div class="task-name">${task.name}</div>
                        <div class="task-meta">Score: ${task.score?.toFixed(1) || 'N/A'}</div>
                    </div>
                    <div class="${priorityClass}">${task.priority || 'medium'}</div>
                </div>
            `;
        });

        container.innerHTML = html;
    }

    startAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
        }

        this.refreshTimer = setInterval(() => {
            this.refreshData();
        }, this.refreshInterval);

        console.log(`⏱️ Auto-refresh started (interval: ${this.refreshInterval}ms)`);
    }

    stopAutoRefresh() {
        if (this.refreshTimer) {
            clearInterval(this.refreshTimer);
            this.refreshTimer = null;
            console.log('⏹️ Auto-refresh stopped');
        }
    }

    showError(message) {
        const statusIndicator = document.querySelector('.status-indicator');
        if (statusIndicator) {
            statusIndicator.setAttribute('data-status', 'error');
            statusIndicator.querySelector('.status-text').textContent = `❌ ${message}`;
        }
    }

    viewLog() {
        window.open('/api/logs/autonomous-improvement', '_blank');
    }
}

// Initialize dashboard when DOM is ready
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            window.autonomousImprovementDashboard = new AutonomousImprovementDashboard();
        });
    } else {
        window.autonomousImprovementDashboard = new AutonomousImprovementDashboard();
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AutonomousImprovementDashboard;
}
