"""
BLACKBOX5 Autonomous Discovery System

Automatically discovers, evaluates, and integrates new skills and frameworks
from GitHub, the internet, and other sources to enable recursive self-improvement.
"""

import asyncio
import logging
import json
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from pathlib import Path
import httpx
from github import Github
import yaml

logger = logging.getLogger(__name__)


@dataclass
class DiscoveredSkill:
    """Represents a discovered skill"""
    name: str
    source: str  # github, url, local
    repository: Optional[str] = None
    description: str = ""
    category: str = "uncategorized"
    url: str = ""

    # Evaluation
    stars: int = 0
    last_updated: Optional[str] = None
    license: str = "unknown"

    # Compatibility
    compatibility_score: float = 0.0  # 0-100
    integration_complexity: str = "unknown"  # low, medium, high

    # Status
    status: str = "discovered"  # discovered, evaluating, integrating, integrated, rejected
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())
    evaluated_at: Optional[str] = None
    integrated_at: Optional[str] = None

    # Analysis
    analysis_notes: List[str] = field(default_factory=list)
    integration_steps: List[str] = field(default_factory=list)
    requirements: List[str] = field(default_factory=list)


@dataclass
class DiscoveredFramework:
    """Represents a discovered agent framework"""
    name: str
    source: str
    repository: Optional[str] = None
    description: str = ""
    url: str = ""

    # Evaluation
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    last_updated: Optional[str] = None

    # Capabilities
    capabilities: List[str] = field(default_factory=list)
    supports_multimodal: bool = False
    supports_parallel: bool = False
    has_memory: bool = False

    # Status
    status: str = "discovered"
    discovered_at: str = field(default_factory=lambda: datetime.now().isoformat())


class GitHubDiscovery:
    """Discover skills and frameworks from GitHub"""

    def __init__(self, github_token: Optional[str] = None):
        self.github_token = github_token
        self.gh = Github(github_token) if github_token else Github()

    async def search_agent_repositories(
        self,
        query: str = "agent framework",
        max_results: int = 20
    ) -> List[DiscoveredFramework]:
        """Search GitHub for agent framework repositories"""
        frameworks = []

        try:
            repos = self.gh.search_repositories(
                query=query,
                sort="stars",
                order="desc"
            )

            for repo in list(repos)[:max_results]:
                framework = DiscoveredFramework(
                    name=repo.name,
                    source="github",
                    repository=repo.full_name,
                    description=repo.description or "",
                    url=repo.html_url,
                    stars=repo.stargazers_count,
                    forks=repo.forks_count,
                    open_issues=repo.open_issues_count,
                    last_updated=repo.updated_at.isoformat() if repo.updated_at else None
                )

                # Analyze capabilities from description and topics
                desc_lower = framework.description.lower()
                if "multimodal" in desc_lower:
                    framework.supports_multimodal = True
                if "parallel" in desc_lower:
                    framework.supports_parallel = True
                if "memory" in desc_lower:
                    framework.has_memory = True

                # Get topics
                try:
                    topics = repo.get_topics()
                    framework.capabilities.extend(topics)
                except:
                    pass

                frameworks.append(framework)
                logger.info(f"Discovered framework: {framework.name} ({framework.stars} stars)")

        except Exception as e:
            logger.error(f"Error searching GitHub: {e}")

        return frameworks

    async def search_skill_files(
        self,
        query: str = "filename:skill.md OR filename:SKILL.md language:Markdown",
        max_results: int = 30
    ) -> List[DiscoveredSkill]:
        """Search GitHub for skill definition files"""
        skills = []

        try:
            # Search for code/skill files
            code_results = self.gh.search_code(
                query=query,
                order="desc"
            )

            for file in list(code_results)[:max_results]:
                try:
                    # Get file content
                    content = file.decoded_content.decode('utf-8')

                    skill = DiscoveredSkill(
                        name=file.name.replace('.md', ''),
                        source="github",
                        repository=file.repository.full_name,
                        description=content[:200] if content else "",
                        url=file.html_url,
                        stars=file.repository.stargazers_count,
                        last_updated=file.repository.updated_at.isoformat() if file.repository.updated_at else None
                    )

                    skills.append(skill)
                    logger.info(f"Discovered skill: {skill.name} from {skill.repository}")

                except Exception as e:
                    logger.warning(f"Error processing file {file.path}: {e}")
                    continue

        except Exception as e:
            logger.error(f"Error searching for skill files: {e}")

        return skills


class SkillEvaluator:
    """Evaluate discovered skills for compatibility and value"""

    async def evaluate_skill(self, skill: DiscoveredSkill) -> float:
        """Evaluate a skill and return compatibility score (0-100)"""

        score = 0.0
        notes = []

        # Check description quality (0-20 points)
        if len(skill.description) > 100:
            score += 10
        if "how to" in skill.description.lower() or "guide" in skill.description.lower():
            score += 10
            notes.append("Contains instructional content")

        # Check repository activity (0-30 points)
        if skill.stars > 100:
            score += 15
            notes.append(f"Popular repository ({skill.stars} stars)")
        elif skill.stars > 10:
            score += 5

        if skill.last_updated:
            last_updated = datetime.fromisoformat(skill.last_updated)
            if (datetime.now() - last_updated).days < 90:
                score += 15
                notes.append("Recently updated")
            elif (datetime.now() - last_updated).days < 365:
                score += 10
            else:
                notes.append("Not recently updated")

        # Check category fit (0-20 points)
        relevant_categories = [
            "automation", "integration", "development",
            "documentation", "collaboration", "testing"
        ]
        if skill.category.lower() in relevant_categories:
            score += 20
            notes.append("Relevant category")

        # Check license (0-30 points)
        if skill.license in ["mit", "apache-2.0", "bsd-3-clause"]:
            score += 30
            notes.append("Permissive license")
        elif skill.license == "unknown":
            notes.append("License unknown - needs verification")

        skill.compatibility_score = score
        skill.analysis_notes = notes

        return score

    async def evaluate_framework(self, framework: DiscoveredFramework) -> float:
        """Evaluate a framework and return compatibility score (0-100)"""

        score = 0.0
        notes = []

        # Popularity (0-30 points)
        if framework.stars > 10000:
            score += 30
            notes.append("Highly popular framework")
        elif framework.stars > 1000:
            score += 20
        elif framework.stars > 100:
            score += 10

        # Activity (0-20 points)
        if framework.last_updated:
            last_updated = datetime.fromisoformat(framework.last_updated)
            if (datetime.now() - last_updated).days < 30:
                score += 20
                notes.append("Very active development")
            elif (datetime.now() - last_updated).days < 90:
                score += 15
            elif (datetime.now() - last_updated).days < 365:
                score += 10

        # Capabilities (0-30 points)
        if framework.supports_multimodal:
            score += 10
        if framework.supports_parallel:
            score += 10
        if framework.has_memory:
            score += 10

        # Community engagement (0-20 points)
        if framework.forks > 1000:
            score += 10
        if framework.open_issues < 100:
            score += 10

        return score


class SkillIntegrator:
    """Integrate discovered skills into BLACKBOX5"""

    def __init__(self, blackbox5_path: Path):
        self.blackbox5_path = blackbox5_path
        self.skills_dir = blackbox5_path / "2-engine" / "04-skills"

    async def integrate_skill(self, skill: DiscoveredSkill) -> bool:
        """Integrate a skill into BLACKBOX5"""

        logger.info(f"Integrating skill: {skill.name}")

        try:
            # Determine target category directory
            target_dir = self._get_category_dir(skill.category)
            target_dir.mkdir(parents=True, exist_ok=True)

            # Create skill file
            skill_file = target_dir / f"{skill.name}.md"

            # Skip if already exists
            if skill_file.exists():
                logger.warning(f"Skill {skill.name} already exists, skipping")
                return False

            # Write skill content
            content = self._generate_skill_content(skill)
            skill_file.write_text(content)

            skill.status = "integrated"
            skill.integrated_at = datetime.now().isoformat()

            logger.info(f"Successfully integrated skill: {skill.name} -> {skill_file}")
            return True

        except Exception as e:
            logger.error(f"Failed to integrate skill {skill.name}: {e}")
            skill.status = "rejected"
            skill.analysis_notes.append(f"Integration failed: {e}")
            return False

    def _get_category_dir(self, category: str) -> Path:
        """Map category to directory"""
        category_map = {
            "automation": "01-automation",
            "integration": "02-integrations",
            "development": "03-development",
            "documentation": "04-documentation",
            "collaboration": "05-collaboration",
            "testing": "06-testing",
            "uncategorized": "00-uncategorized"
        }
        dir_name = category_map.get(category.lower(), "00-uncategorized")
        return self.skills_dir / dir_name

    def _generate_skill_content(self, skill: DiscoveredSkill) -> str:
        """Generate skill file content"""
        return f"""# {skill.name}

**Source:** {skill.url}
**Discovered:** {skill.discovered_at}
**Repository:** {skill.repository or 'N/A'}
**License:** {skill.license}

## Description

{skill.description}

## Evaluation

- **Compatibility Score:** {skill.compatibility_score:.1f}/100
- **Integration Complexity:** {skill.integration_complexity}

## Analysis Notes

{chr(10).join(f"- {note}" for note in skill.analysis_notes) if skill.analysis_notes else "None"}

## Integration Steps

{chr(10).join(f"{i+1}. {step}" for i, step in enumerate(skill.integration_steps)) if skill.integration_steps else "To be determined"}

## Requirements

{chr(10).join(f"- {req}" for req in skill.requirements) if skill.requirements else "None specified"}

---

*Auto-generated by BLACKBOX5 Discovery System*
"""


class AutonomousDiscovery:
    """
    Main autonomous discovery system

    Coordinates discovery, evaluation, and integration of skills and frameworks
    for recursive self-improvement.
    """

    def __init__(self, github_token: Optional[str] = None, blackbox5_path: Optional[Path] = None):
        self.github_discovery = GitHubDiscovery(github_token)
        self.evaluator = SkillEvaluator()
        self.integrator = SkillIntegrator(blackbox5_path or Path("./blackbox5"))
        self.discovered_skills: List[DiscoveredSkill] = []
        self.discovered_frameworks: List[DiscoveredFramework] = []
        self.state_file = Path("./.runtime/discovery_state.json")

    async def run_discovery_cycle(self) -> Dict[str, Any]:
        """Run a complete discovery cycle"""

        logger.info("=" * 60)
        logger.info("Starting autonomous discovery cycle")
        logger.info("=" * 60)

        results = {
            "skills_discovered": 0,
            "skills_evaluated": 0,
            "skills_integrated": 0,
            "frameworks_discovered": 0,
            "frameworks_evaluated": 0,
            "start_time": datetime.now().isoformat()
        }

        # Discover frameworks
        logger.info("Discovering frameworks from GitHub...")
        frameworks = await self.github_discovery.search_agent_repositories(max_results=10)
        self.discovered_frameworks.extend(frameworks)
        results["frameworks_discovered"] = len(frameworks)

        # Discover skills
        logger.info("Discovering skills from GitHub...")
        skills = await self.github_discovery.search_skill_files(max_results=20)
        self.discovered_skills.extend(skills)
        results["skills_discovered"] = len(skills)

        # Evaluate skills
        logger.info("Evaluating discovered skills...")
        high_value_skills = []
        for skill in skills:
            score = await self.evaluator.evaluate_skill(skill)
            results["skills_evaluated"] += 1
            skill.status = "evaluated"
            skill.evaluated_at = datetime.now().isoformat()

            if score > 50:  # Only integrate high-value skills
                high_value_skills.append(skill)
                logger.info(f"High-value skill: {skill.name} (score: {score:.1f})")

        # Integrate high-value skills
        logger.info(f"Integrating {len(high_value_skills)} high-value skills...")
        for skill in high_value_skills:
            if await self.integrator.integrate_skill(skill):
                results["skills_integrated"] += 1

        # Save state
        await self.save_state()

        results["end_time"] = datetime.now().isoformat()

        logger.info("=" * 60)
        logger.info("Discovery cycle complete")
        logger.info(f"Frameworks: {results['frameworks_discovered']} discovered")
        logger.info(f"Skills: {results['skills_discovered']} discovered, "
                   f"{results['skills_evaluated']} evaluated, "
                   f"{results['skills_integrated']} integrated")
        logger.info("=" * 60)

        return results

    async def save_state(self):
        """Save discovery state to file"""
        try:
            state = {
                "discovered_skills": [
                    {
                        "name": s.name,
                        "source": s.source,
                        "repository": s.repository,
                        "description": s.description,
                        "compatibility_score": s.compatibility_score,
                        "status": s.status,
                        "discovered_at": s.discovered_at
                    }
                    for s in self.discovered_skills
                ],
                "discovered_frameworks": [
                    {
                        "name": f.name,
                        "repository": f.repository,
                        "stars": f.stars,
                        "status": f.status,
                        "discovered_at": f.discovered_at
                    }
                    for f in self.discovered_frameworks
                ],
                "last_updated": datetime.now().isoformat()
            }

            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, 'w') as f:
                json.dump(state, f, indent=2)

        except Exception as e:
            logger.error(f"Failed to save state: {e}")


# Autonomous discovery task for the scheduler

async def autonomous_discovery_task() -> Dict[str, Any]:
    """Task: Run autonomous discovery cycle"""
    discovery = AutonomousDiscovery()
    results = await discovery.run_discovery_cycle()
    return results
