"""
Five Whys Analyzer for Thought Loop Framework
=============================================

Root cause analysis through systematic questioning.
Addresses the "breaking down logic" requirement by drilling to root causes.
"""

from typing import List, Dict, Optional
from dataclasses import dataclass

try:
    from .models import Assumption, AssumptionType
except ImportError:
    from models import Assumption, AssumptionType


@dataclass
class WhyLevel:
    """A single level in the Five Whys analysis"""
    level: int
    question: str
    answer: str
    confidence: float
    evidence: List[str]
    is_root_cause: bool


@dataclass
class FiveWhysResult:
    """Result of Five Whys analysis"""
    problem: str
    levels: List[WhyLevel]
    root_cause: str
    root_cause_type: str  # 'systemic', 'process', 'human_error', 'technical'
    suggested_solutions: List[str]
    confidence: float


class FiveWhysAnalyzer:
    """
    Performs root cause analysis using the Five Whys technique.

    Addresses the "breaking down logic" requirement by:
    1. Systematically drilling down to root causes
    2. Identifying systemic vs. surface issues
    3. Generating targeted solutions
    4. Preventing superficial analysis
    """

    def __init__(self, max_depth: int = 5):
        """
        Initialize Five Whys analyzer.

        Args:
            max_depth: Maximum depth to drill (default 5)
        """
        self.max_depth = max_depth

    def analyze(self, problem: str, context: str = "") -> FiveWhysResult:
        """
        Perform Five Whys analysis on a problem.

        Args:
            problem: The problem statement
            context: Additional context

        Returns:
            FiveWhysResult with full analysis
        """
        levels = []
        current_question = f"Why is there a problem: {problem}?"

        for i in range(1, self.max_depth + 1):
            # Generate question
            if i > 1:
                current_question = self._generate_why_question(levels[-1].answer, i)

            # Generate answer (in practice, would be provided or researched)
            answer = self._generate_answer(current_question, context)

            # Assess if this might be a root cause
            is_root = self._is_potential_root_cause(answer, i)

            # Create level
            level = WhyLevel(
                level=i,
                question=current_question,
                answer=answer,
                confidence=self._assess_confidence(answer, i),
                evidence=[],
                is_root_cause=is_root
            )
            levels.append(level)

            # Stop if we've reached a root cause
            if is_root:
                break

        # Determine root cause
        root_cause, root_cause_type = self._identify_root_cause(levels)

        # Generate solutions
        solutions = self._generate_solutions(root_cause, root_cause_type, levels)

        # Calculate overall confidence
        confidence = self._calculate_overall_confidence(levels)

        return FiveWhysResult(
            problem=problem,
            levels=levels,
            root_cause=root_cause,
            root_cause_type=root_cause_type,
            suggested_solutions=solutions,
            confidence=confidence
        )

    def analyze_with_answers(self, problem: str,
                             answers: List[str]) -> FiveWhysResult:
        """
        Perform Five Whys with provided answers.

        Args:
            problem: The problem statement
            answers: List of answers to "why" questions

        Returns:
            FiveWhysResult with analysis
        """
        levels = []

        for i, answer in enumerate(answers[:self.max_depth], start=1):
            # Generate question
            if i == 1:
                question = f"Why is there a problem: {problem}?"
            else:
                question = f"And why is that: {levels[-1].answer}?"

            # Assess if root cause
            is_root = self._is_potential_root_cause(answer, i)

            level = WhyLevel(
                level=i,
                question=question,
                answer=answer,
                confidence=0.7,  # Provided answers have higher confidence
                evidence=[],
                is_root_cause=is_root
            )
            levels.append(level)

            if is_root:
                break

        # Determine root cause
        root_cause, root_cause_type = self._identify_root_cause(levels)

        # Generate solutions
        solutions = self._generate_solutions(root_cause, root_cause_type, levels)

        # Calculate confidence
        confidence = self._calculate_overall_confidence(levels)

        return FiveWhysResult(
            problem=problem,
            levels=levels,
            root_cause=root_cause,
            root_cause_type=root_cause_type,
            suggested_solutions=solutions,
            confidence=confidence
        )

    def validate_depth(self, problem: str, current_depth: int,
                       last_answer: str) -> Dict[str, any]:
        """
        Validate if we've drilled deep enough.

        Args:
            problem: Original problem
            current_depth: Current depth level
            last_answer: Last answer given

        Returns:
            Dict with validation results
        """
        validation = {
            'should_continue': True,
            'reason': '',
            'suggested_next_question': '',
            'confidence_sufficient': False
        }

        # Check if we've reached max depth
        if current_depth >= self.max_depth:
            validation['should_continue'] = False
            validation['reason'] = 'Reached maximum analysis depth'
            return validation

        # Check if last answer indicates root cause
        is_root = self._is_potential_root_cause(last_answer, current_depth)

        if is_root:
            validation['should_continue'] = False
            validation['reason'] = 'Root cause identified'
            validation['confidence_sufficient'] = True
            return validation

        # Check if last answer is too vague
        if len(last_answer) < 20:
            validation['reason'] = 'Answer is too vague - need more detail'
            validation['suggested_next_question'] = f"Can you be more specific about why: {last_answer}?"
            return validation

        # Generate next question
        validation['suggested_next_question'] = f"And why is that: {last_answer}?"

        return validation

    def check_for_blame(self, levels: List[WhyLevel]) -> List[str]:
        """
        Check if analysis is blaming individuals instead of systems.

        Args:
            levels: The analysis levels to check

        Returns:
            List of warnings about blame-focused analysis
        """
        warnings = []

        blame_indicators = [
            'because he', 'because she', 'because they',
            'human error', 'user error', 'operator error',
            'failed to', 'didn\'t', 'negligence', 'careless'
        ]

        for level in levels:
            answer_lower = level.answer.lower()

            for indicator in blame_indicators:
                if indicator in answer_lower:
                    warnings.append(
                        f"Level {level.level}: '{indicator}' detected - "
                        "focus on system/process issues, not individual blame"
                    )
                    break

        return warnings

    def _generate_why_question(self, previous_answer: str, level: int) -> str:
        """Generate the next "why" question."""
        if level == 2:
            return f"Why is that: {previous_answer}?"
        else:
            return f"And why is that: {previous_answer}?"

    def _generate_answer(self, question: str, context: str) -> str:
        """
        Generate an answer to a why question.

        In practice, this would involve:
        - Research
        - Consulting experts
        - Analyzing data
        - Examining systems

        For this implementation, we provide a template answer.
        """
        # This is a placeholder - in practice would use actual research
        return "[Analysis required - this would be answered through research/data analysis]"

    def _is_potential_root_cause(self, answer: str, level: int) -> bool:
        """Check if answer represents a root cause."""
        # Root cause indicators
        root_cause_indicators = [
            'no process', 'lack of', 'missing', 'systemic',
            'policy', 'procedure', 'design', 'architecture',
            'culture', 'training', 'resource allocation'
        ]

        answer_lower = answer.lower()

        # Check for systemic indicators
        for indicator in root_cause_indicators:
            if indicator in answer_lower:
                return True

        # At depth 5, likely a root cause
        if level >= 5:
            return True

        # Avoid "human error" as root cause
        blame_indicators = ['because he', 'because she', 'human error', 'user error']
        for indicator in blame_indicators:
            if indicator in answer_lower:
                return False  # Don't stop at human error - go deeper

        return False

    def _assess_confidence(self, answer: str, level: int) -> float:
        """Assess confidence in an answer."""
        # Lower confidence at deeper levels without evidence
        base_confidence = 0.8
        depth_penalty = (level - 1) * 0.1

        return max(0.3, base_confidence - depth_penalty)

    def _identify_root_cause(self, levels: List[WhyLevel]) -> tuple:
        """Identify the root cause and its type."""
        if not levels:
            return "", "unknown"

        # Get the last level marked as root cause, or the deepest level
        root_level = None
        for level in reversed(levels):
            if level.is_root_cause:
                root_level = level
                break

        if not root_level:
            root_level = levels[-1]

        # Classify root cause type
        root_cause_type = self._classify_root_cause(root_level.answer)

        return root_level.answer, root_cause_type

    def _classify_root_cause(self, answer: str) -> str:
        """Classify the type of root cause."""
        answer_lower = answer.lower()

        if any(word in answer_lower for word in ['process', 'procedure', 'workflow']):
            return 'process'

        if any(word in answer_lower for word in ['system', 'design', 'architecture', 'infrastructure']):
            return 'systemic'

        if any(word in answer_lower for word in ['training', 'skill', 'knowledge', 'education']):
            return 'human_error'  # But as training issue, not blame

        if any(word in answer_lower for word in ['bug', 'code', 'implementation', 'technical']):
            return 'technical'

        if any(word in answer_lower for word in ['policy', 'rule', 'governance']):
            return 'process'

        return 'systemic'  # Default

    def _generate_solutions(self, root_cause: str, root_cause_type: str,
                            levels: List[WhyLevel]) -> List[str]:
        """Generate solutions based on root cause."""
        solutions = []

        # Generate solutions based on type
        if root_cause_type == 'process':
            solutions.extend([
                "Review and update the relevant process",
                "Add process validation steps",
                "Implement process monitoring"
            ])

        elif root_cause_type == 'systemic':
            solutions.extend([
                "Redesign the system architecture",
                "Address systemic barriers",
                "Implement systemic safeguards"
            ])

        elif root_cause_type == 'human_error':
            solutions.extend([
                "Provide additional training",
                "Improve documentation",
                "Implement validation checks"
            ])

        elif root_cause_type == 'technical':
            solutions.extend([
                "Fix the underlying technical issue",
                "Add automated tests",
                "Implement monitoring"
            ])

        # Add specific solution based on root cause
        solutions.append(f"Address: {root_cause}")

        return solutions

    def _calculate_overall_confidence(self, levels: List[WhyLevel]) -> float:
        """Calculate overall confidence in the analysis."""
        if not levels:
            return 0.0

        # Average confidence across levels
        avg_confidence = sum(level.confidence for level in levels) / len(levels)

        # Reduce confidence if we stopped early
        if len(levels) < 3:
            avg_confidence *= 0.7

        return avg_confidence
