const express = require('express');
const cors = require('cors');
const axios = require('axios');
const http = require('http');

const PORT = process.env.PORT || 8001;

const app = express();

app.use(cors());

// Simple in-memory agent store
let agents = [
    {
        id: 'blackbox5-scribe',
        name: 'BlackBox5 Scribe',
        description: 'Documents all tasks, decisions, and knowledge',
        status: 'idle',
        task: null,
        uptime: '0m',
        tokensUsed: 0
    }
];

app.get('/api/agents', (req, res) => {
    res.json(agents);
});

app.post('/api/agents/start', async (req, res) => {
    const { agentId } = req.body;
    const agent = agents.find(a => a.id === agentId);
    if (!agent) {
        return res.status(404).json({ success: false, error: 'Agent not found' });
    }
    
    // Start agent via OpenClaw CLI
    try {
        const { exec } = require('child_process');
        exec(`openclaw session start agent:${agentId}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error starting agent: ${error}`);
                return res.status(500).json({ success: false, error: error.message });
            }
            
            agent.status = 'running';
            agent.task = 'Started via dashboard';
            agents = agents; // Update store
            res.json({ success: true, agentId, message: `Agent ${agent.name} started` });
        });
    } catch (error) {
        console.error('Error starting agent:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.post('/api/agents/stop', async (req, res) => {
    const { agentId } = req.body;
    const agent = agents.find(a => a.id === agentId);
    if (!agent) {
        return res.status(404).json({ success: false, error: 'Agent not found' });
    }
    
    // Stop agent via OpenClaw CLI
    try {
        const { exec } = require('child_process');
        exec(`openclaw session kill agent:${agentId}`, (error, stdout, stderr) => {
            if (error) {
                console.error(`Error stopping agent: ${error}`);
                return res.status(500).json({ success: false, error: error.message });
            }
            
            agent.status = 'idle';
            agent.task = 'Stopped by dashboard';
            agents = agents; // Update store
            res.json({ success: true, agentId, message: `Agent ${agent.name} stopped` });
        });
    } catch (error) {
        console.error('Error stopping agent:', error);
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(PORT, () => {
    console.log(`BlackBox5 Gateway server running on port ${PORT}`);
});
