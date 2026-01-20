/**
 * Sequential Thinking MCP Server - HTTP Wrapper for Railway
 *
 * This wrapper exposes the Sequential Thinking MCP server over HTTP
 * for deployment on Railway.app or similar platforms.
 */

import express from 'express';
import { Server } from '@modelcontextprotocol/server-sequential-thinking';

const app = express();
app.use(express.json());

const PORT = process.env.PORT || 3000;

// Initialize the Sequential Thinking MCP server
let mcpServer;

try {
  mcpServer = new Server();
  console.log('Sequential Thinking MCP Server initialized');
} catch (error) {
  console.error('Failed to initialize MCP server:', error);
  process.exit(1);
}

// Health check endpoint (Railway requires this)
app.get('/health', (req, res) => {
  res.json({
    status: 'healthy',
    service: 'mcp-sequential-thinking',
    timestamp: new Date().toISOString()
  });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    service: 'Sequential Thinking MCP Server',
    version: '1.0.0',
    endpoints: {
      health: '/health',
      mcp: '/' // MCP protocol endpoint
    }
  });
});

// MCP protocol endpoint
// Note: The actual MCP server implementation may need to be adapted
// based on how @modelcontextprotocol/server-sequential-thinking exposes its interface
app.post('/', async (req, res) => {
  try {
    console.log('Received MCP request:', JSON.stringify(req.body, null, 2));

    // The MCP server typically communicates via stdio
    // For HTTP transport, we need to handle the request differently
    // This is a placeholder that shows the structure

    // For now, return a basic response structure
    // You'll need to adapt this based on the actual MCP server's API

    const response = {
      jsonrpc: "2.0",
      id: req.body.id || null,
      result: {
        content: [{
          type: "text",
          text: "Sequential thinking MCP server is running"
        }]
      }
    };

    res.json(response);
  } catch (error) {
    console.error('Error handling MCP request:', error);
    res.status(500).json({
      jsonrpc: "2.0",
      id: req.body.id || null,
      error: {
        code: -32603,
        message: "Internal error",
        data: error.message
      }
    });
  }
});

// Start the server
app.listen(PORT, () => {
  console.log(`Sequential Thinking MCP Server listening on port ${PORT}`);
  console.log(`Health check available at http://localhost:${PORT}/health`);
});
