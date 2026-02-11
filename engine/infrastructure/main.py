"""
BlackBox5 Main Entry Point

Provides the primary interface for accessing the BlackBox5 system.
This module initializes and manages core components including agents,
skill managers, and guide registries.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional

# Set up logging
logger = logging.getLogger(__name__)

# Singleton instance
_blackbox5_instance: Optional['BlackBox5'] = None


class BlackBox5:
    """
    Main BlackBox5 system interface.
    
    Provides access to:
    - Agent management
    - Skill management
    - Guide registry
    - Request processing
    """
    
    def __init__(self):
        """Initialize the BlackBox5 system."""
        self._agents: Dict[str, Any] = {}
        self._skill_manager: Optional[Any] = None
        self._guide_registry: Optional[Any] = None
        self._initialized = False
        
    async def initialize(self):
        """Initialize all system components."""
        if self._initialized:
            return
            
        logger.info("Initializing BlackBox5 system...")
        
        # Initialize agent loader and load agents
        try:
            from agents.framework.agent_loader import AgentLoader
            agent_loader = AgentLoader()
            loaded_agents = await agent_loader.load_all()
            self._agents = loaded_agents
            logger.info(f"Loaded {len(self._agents)} agents")
        except Exception as e:
            logger.warning(f"Could not load agents: {e}")
            self._agents = {}
        
        # Initialize skill manager
        try:
            from agents.framework.skill_manager import SkillManager
            self._skill_manager = SkillManager()
            await self._skill_manager.load_all()
            logger.info("Skill manager initialized")
        except Exception as e:
            logger.warning(f"Could not initialize skill manager: {e}")
            self._skill_manager = None
        
        # Initialize guide registry (placeholder - implement as needed)
        self._guide_registry = None

        # Keyword to agent mapping for smart routing
        self._routing_keywords = {
            'database': ['database', 'schema', 'postgres', 'mysql', 'query', 'table', 'migration'],
            'security': ['security', 'vulnerability', 'audit', 'penetration', 'owasp', 'auth', 'encrypt', 'injection', 'xss', 'csrf', 'breach', 'exploit'],
            'frontend': ['react', 'vue', 'angular', 'frontend', 'ui', 'css', 'html', 'component', 'dom'],
            'backend': ['api', 'backend', 'server', 'endpoint', 'rest', 'graphql', 'microservice'],
            'devops': ['docker', 'kubernetes', 'k8s', 'ci/cd', 'pipeline', 'deploy', 'infrastructure', 'terraform'],
            'testing': ['test', 'testing', 'pytest', 'jest', 'cypress', 'unit test', 'integration test'],
            'performance': ['performance', 'optimization', 'slow', 'bottleneck', 'cache', 'latency'],
            'ml': ['machine learning', 'ml', 'ai model', 'tensorflow', 'pytorch', 'neural', 'training'],
            'mobile': ['mobile', 'ios', 'android', 'react native', 'flutter', 'app'],
            'data': ['data', 'analytics', 'etl', 'pipeline', 'warehouse', 'bigquery', 'snowflake'],
        }

        # Security keywords that should override other matches
        self._security_override = ['injection', 'xss', 'csrf', 'vulnerability', 'exploit', 'breach', 'penetration']

        self._initialized = True
        logger.info("BlackBox5 system initialized")

    def _route_request(self, query: str, forced_agent: Optional[str], strategy: str) -> tuple:
        """Route request to appropriate agent based on query content."""
        query_lower = query.lower()

        # If agent is forced and exists, use it
        if forced_agent:
            if forced_agent in self._agents:
                return self._agents[forced_agent], {
                    'strategy': 'single_agent',
                    'agent': forced_agent,
                    'complexity': 0.5,
                    'confidence': 0.9
                }
            else:
                # Invalid agent - return error
                return None, {'strategy': 'none', 'agent': forced_agent, 'error': f'Agent "{forced_agent}" not found'}

        # Try keyword matching
        best_match = None
        best_score = 0

        # Check for security override keywords first
        for sec_keyword in self._security_override:
            if sec_keyword in query_lower:
                # Force security specialist if security keywords found
                for agent_name in self._agents.keys():
                    if 'security' in agent_name.lower():
                        return self._agents[agent_name], {
                            'strategy': 'single_agent',
                            'agent': agent_name,
                            'complexity': 0.5,
                            'confidence': 0.9
                        }

        for agent_name, agent in self._agents.items():
            score = 0

            # Check agent capabilities
            caps = getattr(agent, 'config', None)
            if caps and hasattr(caps, 'capabilities'):
                for cap in caps.capabilities:
                    if cap.lower() in query_lower:
                        score += 2

            # Check routing keywords
            for category, keywords in self._routing_keywords.items():
                if category in agent_name.lower():
                    for keyword in keywords:
                        if keyword in query_lower:
                            score += 3

            if score > best_score:
                best_score = score
                best_match = agent_name

        # If we found a match, use it
        if best_match:
            return self._agents[best_match], {
                'strategy': 'single_agent',
                'agent': best_match,
                'complexity': 0.5,
                'confidence': min(0.5 + (best_score * 0.1), 0.95)
            }

        # Fallback: use DeveloperAgent if available, otherwise first agent
        if 'DeveloperAgent' in self._agents:
            return self._agents['DeveloperAgent'], {
                'strategy': 'single_agent',
                'agent': 'DeveloperAgent',
                'complexity': 0.5,
                'confidence': 0.6
            }
        elif self._agents:
            first = list(self._agents.keys())[0]
            return self._agents[first], {
                'strategy': 'single_agent',
                'agent': first,
                'complexity': 0.5,
                'confidence': 0.5
            }

        return None, {'strategy': 'none', 'agent': None, 'error': 'No agents available'}
    
    async def process_request(
        self, 
        query: str, 
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process a user request.
        
        Args:
            query: The user's query or task
            session_id: Optional session ID for continuity
            context: Optional context dictionary
            
        Returns:
            Dictionary containing the result and metadata
        """
        if not self._initialized:
            await self.initialize()
        
        context = context or {}
        
        # Determine execution strategy
        strategy = context.get('strategy', 'auto')
        forced_agent = context.get('forced_agent')
        
        # Smart routing logic with keyword matching
        agent, routing = self._route_request(query, forced_agent, strategy)

        if agent is None:
            # No agents available
            return {
                'success': False,
                'error': 'No agents available',
                'routing': {'strategy': 'none', 'agent': None},
                'session_id': session_id,
                'timestamp': str(asyncio.get_event_loop().time())
            }
        
        # Process the request
        try:
            # Create agent task and execute
            from agents.framework.base_agent import AgentTask
            task = AgentTask(
                id=f"task-{asyncio.get_event_loop().time()}",
                description=query,
                type="general",
                complexity="medium",
                context=context
            )

            # Execute via agent
            agent_result = await agent.execute(task)

            result = {
                'success': agent_result.success,
                'output': agent_result.output,
                'error': agent_result.error,
                'metadata': {
                    'agent_used': routing['agent'],
                    'strategy': routing['strategy'],
                    'thinking_steps': agent_result.thinking_steps,
                    'artifacts': agent_result.artifacts,
                    'duration': agent_result.duration
                }
            }
        except Exception as e:
            logger.error(f"Error processing request: {e}")
            result = {
                'success': False,
                'output': '',
                'error': str(e),
                'metadata': {}
            }
        
        return {
            'result': result,
            'routing': routing,
            'session_id': session_id or 'default',
            'timestamp': str(asyncio.get_event_loop().time()),
            'guide_suggestions': []
        }


async def get_blackbox5() -> BlackBox5:
    """
    Get the singleton BlackBox5 instance.
    
    Returns:
        Initialized BlackBox5 instance
    """
    global _blackbox5_instance
    
    if _blackbox5_instance is None:
        _blackbox5_instance = BlackBox5()
        await _blackbox5_instance.initialize()
    
    return _blackbox5_instance
