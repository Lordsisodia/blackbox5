"""
Socratic Questioner for Thought Loop Framework
==============================================

Systematic questioning framework to deepen analysis, uncover assumptions,
and stimulate critical thinking. Addresses the "thinking logically" requirement.
"""

from typing import List, Dict
from dataclasses import dataclass
import re

try:
    from .models import Assumption, AssumptionType
except ImportError:
    from models import Assumption, AssumptionType


@dataclass
class SocraticQuestion:
    """A generated Socratic question"""
    question: str
    question_type: str  # clarification, assumptions, evidence, perspectives, implications, meta
    target: str  # What the question is targeting (term, claim, etc.)


@dataclass
class DialogueRound:
    """A round of Socratic dialogue"""
    round_number: int
    question_type: str
    questions: List[str]
    purpose: str


@dataclass
class QuestioningSession:
    """A complete Socratic questioning session"""
    statement: str
    rounds: List[DialogueRound]
    total_questions: int
    uncovered_assumptions: List[str]
    suggested_research: List[str]


class SocraticQuestioner:
    """
    Systematic Socratic questioning for deeper analysis.

    Addresses the "thinking logically" requirement by:
    1. Generating 6 types of systematic questions
    2. Uncovering hidden assumptions
    3. Examining evidence quality
    4. Exploring alternative perspectives
    5. Considering implications and consequences
    6. Meta-questioning the problem itself
    """

    def __init__(self):
        self.question_templates = self._load_question_templates()

    def question(self, text: str, question_type: str = None,
                 max_questions: int = 5) -> List[str]:
        """
        Generate Socratic questions for given text.

        Args:
            text: The text to question
            question_type: Type of questions to generate (or all types)
            max_questions: Maximum number of questions per type

        Returns:
            List of questions
        """
        questions = []

        # Analyze text to extract key elements
        analysis = self._analyze(text)

        # Generate questions
        if question_type is None:
            question_types = self.question_templates.keys()
        else:
            question_types = [question_type]

        for qtype in question_types:
            type_questions = self._generate_questions(qtype, analysis, max_questions)
            questions.extend(type_questions)

        return questions

    def facilitate_dialogue(self, statement: str, max_rounds: int = 6) -> QuestioningSession:
        """
        Facilitate a complete Socratic dialogue session.

        Args:
            statement: The statement to analyze
            max_rounds: Maximum number of questioning rounds

        Returns:
            QuestioningSession with all rounds and analysis
        """
        session = QuestioningSession(
            statement=statement,
            rounds=[],
            total_questions=0,
            uncovered_assumptions=[],
            suggested_research=[]
        )

        # Define dialogue sequence
        dialogue_sequence = [
            ('clarification', 'Clarify terms and meaning'),
            ('assumptions', 'Uncover underlying assumptions'),
            ('evidence', 'Examine supporting evidence'),
            ('perspectives', 'Explore alternative viewpoints'),
            ('implications', 'Consider consequences'),
            ('meta_questions', 'Question the question itself')
        ]

        for i, (qtype, purpose) in enumerate(dialogue_sequence[:max_rounds]):
            questions = self.question(statement, qtype, max_questions=3)

            if questions:
                session.rounds.append(DialogueRound(
                    round_number=i + 1,
                    question_type=qtype,
                    questions=questions,
                    purpose=purpose
                ))

                session.total_questions += len(questions)

                # Extract assumptions from assumptions round
                if qtype == 'assumptions':
                    session.uncovered_assumptions.extend(
                        self._extract_assumptions_from_questions(questions)
                    )

                # Generate research suggestions from evidence round
                if qtype == 'evidence':
                    session.suggested_research.extend(
                        self._generate_research_suggestions(questions)
                    )

        return session

    def question_assumption(self, assumption: Assumption) -> List[str]:
        """
        Generate specific questions for an assumption.

        Args:
            assumption: The assumption to question

        Returns:
            List of questions targeting the assumption
        """
        questions = []

        # Questions based on assumption type
        if assumption.type == AssumptionType.CRITICAL:
            questions.extend([
                f"What would happen if '{assumption.statement}' is false?",
                f"What evidence do we have that '{assumption.statement}'?",
                f"How could we verify or falsify '{assumption.statement}'?",
            ])
        elif assumption.type == AssumptionType.IMPORTANT:
            questions.extend([
                f"Why do you believe '{assumption.statement}'?",
                f"Is '{assumption.statement}' always true or just sometimes?",
            ])
        else:  # MINOR
            questions.extend([
                f"How important is '{assumption.statement}'?",
                f"Could we proceed even if '{assumption.statement}' is uncertain?",
            ])

        # General assumption questions
        questions.extend([
            f"What are the implications if '{assumption.statement}' is wrong?",
            f"Has '{assumption.statement}' been tested or verified?",
            f"Are there alternative explanations to '{assumption.statement}'?",
        ])

        return questions

    def validate_reasoning_depth(self, reasoning: str,
                                  context: str = "") -> Dict[str, any]:
        """
        Validate that reasoning has sufficient depth.

        Args:
            reasoning: The reasoning text to validate
            context: Optional context

        Returns:
            Dict with depth assessment
        """
        assessment = {
            'depth_score': 0.0,
            'missing_question_types': [],
            'suggestions': [],
            'has_clarification': False,
            'has_evidence_examination': False,
            'has_alternative_consideration': False
        }

        reasoning_lower = reasoning.lower()

        # Check for clarification indicators
        clarification_indicators = ['means', 'defined as', 'refers to', 'specifically']
        assessment['has_clarification'] = any(ind in reasoning_lower for ind in clarification_indicators)

        # Check for evidence examination
        evidence_indicators = ['evidence', 'data', 'research', 'study shows', 'according to']
        assessment['has_evidence_examination'] = any(ind in reasoning_lower for ind in evidence_indicators)

        # Check for alternative consideration
        alternative_indicators = ['alternatively', 'however', 'on the other hand',
                                  'another view', 'different perspective']
        assessment['has_alternative_consideration'] = any(ind in reasoning_lower for ind in alternative_indicators)

        # Calculate depth score
        depth_indicators = [
            assessment['has_clarification'],
            assessment['has_evidence_examination'],
            assessment['has_alternative_consideration']
        ]

        assessment['depth_score'] = sum(depth_indicators) / len(depth_indicators)

        # Identify missing question types
        if not assessment['has_clarification']:
            assessment['missing_question_types'].append('clarification')
            assessment['suggestions'].append('Define key terms clearly')

        if not assessment['has_evidence_examination']:
            assessment['missing_question_types'].append('evidence')
            assessment['suggestions'].append('Examine supporting evidence')

        if not assessment['has_alternative_consideration']:
            assessment['missing_question_types'].append('perspectives')
            assessment['suggestions'].append('Consider alternative viewpoints')

        return assessment

    def _load_question_templates(self) -> Dict[str, List[str]]:
        """Load Socratic question templates"""
        return {
            'clarification': [
                "What do you mean by {term}?",
                "Can you give me an example of {term}?",
                "How would you define {term} in this context?",
                "What exactly do you mean when you say {term}?",
                "How does {term} relate to the problem?",
            ],
            'assumptions': [
                "What are you assuming when you say {statement}?",
                "Why do you believe {statement} is true?",
                "What would have to be true for {statement} to hold?",
                "Is {statement} always true, or just sometimes?",
                "How could you verify or disprove {statement}?",
                "What if {statement} is wrong?",
            ],
            'evidence': [
                "What evidence supports {claim}?",
                "How do you know {claim} is true?",
                "What would count as evidence against {claim}?",
                "Is your source for {claim} reliable?",
                "Are there alternative explanations for {claim}?",
                "How strong is the evidence for {claim}?",
            ],
            'perspectives': [
                "How would {stakeholder} view this?",
                "What would someone who disagrees say?",
                "What's another way to look at {issue}?",
                "What are the strengths of the opposing view?",
                "Can you see this from a different perspective?",
                "What are we missing from our current viewpoint?",
            ],
            'implications': [
                "What would happen if {action}?",
                "What are the consequences of {outcome}?",
                "What's the worst-case scenario here?",
                "What's the best-case scenario?",
                "What are the long-term effects of {decision}?",
                "Who would be affected by this?",
            ],
            'meta_questions': [
                "Why is this question important?",
                "What are we really trying to figure out?",
                "Is this the right question to ask?",
                "What would change if we framed this differently?",
                "What assumptions are built into our question?",
                "Are we solving the right problem?",
            ]
        }

    def _analyze(self, text: str) -> Dict:
        """Analyze text to extract key elements for questioning"""
        return {
            'terms': self._extract_terms(text),
            'claims': self._extract_claims(text),
            'stakeholders': self._extract_stakeholders(text),
            'actions': self._extract_actions(text),
            'issues': self._extract_issues(text)
        }

    def _extract_terms(self, text: str) -> List[str]:
        """Extract key terms that might need clarification"""
        # Look for capitalized words, technical terms, potentially important nouns
        candidates = re.findall(r'\b[A-Z][a-z]+\b', text)

        # Also look for words with quotes or emphasis
        quoted = re.findall(r'["\']([\w\s]+)["\']', text)
        candidates.extend(quoted)

        # Remove duplicates and return
        return list(set(candidates))

    def _extract_claims(self, text: str) -> List[str]:
        """Extract claims that need evidence"""
        # Look for statements with "is", "are", "will", "should"
        patterns = [
            r'[A-Z][^.]+(?:is|are|will|should)[^.]+\.',
            r'[A-Z][^.]+(?:must|cannot|can)[^.]+\.',
        ]

        claims = []
        for pattern in patterns:
            matches = re.findall(pattern, text)
            claims.extend(matches)

        return list(set(claims))

    def _extract_stakeholders(self, text: str) -> List[str]:
        """Extract stakeholders mentioned or implied"""
        # Common stakeholder groups
        stakeholder_patterns = [
            r'\b(customers|users|employees|management|investors|public|stakeholders|clients)\b',
            r'\b(developers|designers|product|team|organization)\b',
        ]

        stakeholders = []
        for pattern in stakeholder_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            stakeholders.extend(matches)

        return list(set(stakeholders))

    def _extract_actions(self, text: str) -> List[str]:
        """Extract actions or decisions"""
        # Look for action verbs
        action_patterns = [
            r'\b(implement|build|create|launch|start|stop|change|modify|optimize)[^.]+\b',
            r'\b(decide|choose|select|reject|accept)[^.]+\b',
        ]

        actions = []
        for pattern in action_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            actions.extend(matches)

        return list(set(actions))

    def _extract_issues(self, text: str) -> List[str]:
        """Extract issues or problems mentioned"""
        # Look for problem indicators
        problem_patterns = [
            r'\b(problem|issue|challenge|concern|difficulty)[^.]+\b',
            r'\b(fail|error|bug|crash|slow)[^.]+\b',
        ]

        issues = []
        for pattern in problem_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            issues.extend(matches)

        return list(set(issues))

    def _generate_questions(self, qtype: str, analysis: Dict,
                           max_questions: int) -> List[str]:
        """Generate questions of a specific type"""
        questions = []
        templates = self.question_templates.get(qtype, [])

        for template in templates:
            # Skip if we've hit max
            if len(questions) >= max_questions:
                break

            # Fill in template based on placeholders
            if '{term}' in template:
                for term in analysis['terms'][:2]:
                    if len(questions) >= max_questions:
                        break
                    questions.append(template.format(term=term))

            elif '{statement}' in template:
                for claim in analysis['claims'][:2]:
                    if len(questions) >= max_questions:
                        break
                    # Truncate long claims
                    claim_short = claim[:50] + "..." if len(claim) > 50 else claim
                    questions.append(template.format(statement=claim_short))

            elif '{claim}' in template:
                for claim in analysis['claims'][:2]:
                    if len(questions) >= max_questions:
                        break
                    claim_short = claim[:50] + "..." if len(claim) > 50 else claim
                    questions.append(template.format(claim=claim_short))

            elif '{stakeholder}' in template:
                for stakeholder in analysis['stakeholders'][:2]:
                    if len(questions) >= max_questions:
                        break
                    questions.append(template.format(stakeholder=stakeholder))

            elif '{issue}' in template:
                for issue in analysis['issues'][:2]:
                    if len(questions) >= max_questions:
                        break
                    questions.append(template.format(issue=issue))

            elif '{action}' in template:
                for action in analysis['actions'][:2]:
                    if len(questions) >= max_questions:
                        break
                    questions.append(template.format(action=action))

            elif '{outcome}' in template:
                questions.append(template.format(outcome="this outcome"))

            elif '{decision}' in template:
                questions.append(template.format(decision="this decision"))

            # Templates with no placeholders
            elif not any(placeholder in template for placeholder in
                        ['{term}', '{statement}', '{claim}', '{stakeholder}',
                         '{issue}', '{action}', '{outcome}', '{decision}']):
                questions.append(template)

        return questions[:max_questions]

    def _extract_assumptions_from_questions(self, questions: List[str]) -> List[str]:
        """Extract implicit assumptions from generated questions"""
        assumptions = []

        for question in questions:
            # Look for "what if X" patterns - these reveal assumptions
            if "what if" in question.lower():
                # Extract what's being questioned
                match = re.search(r'what if (.+?)\??', question, re.IGNORECASE)
                if match:
                    assumptions.append(match.group(1))

            # Look for "why do you believe" patterns
            if "why do you believe" in question.lower():
                match = re.search(r'why do you believe (.+?)\??', question, re.IGNORECASE)
                if match:
                    assumptions.append(match.group(1))

        return list(set(assumptions))

    def _generate_research_suggestions(self, questions: List[str]) -> List[str]:
        """Generate research suggestions based on evidence questions"""
        suggestions = []

        for question in questions:
            # Look for requests for evidence
            if "what evidence" in question.lower():
                suggestions.append(f"Gather evidence to address: {question}")

            if "how do you know" in question.lower():
                suggestions.append(f"Verify knowledge claim: {question}")

            if "source" in question.lower():
                suggestions.append(f"Identify reliable sources: {question}")

        return list(set(suggestions))

