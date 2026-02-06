"""
Learning Extraction Module

Extracts structured learnings from task run directories and manages
the learning-index.yaml knowledge base.

Main Classes:
    LearningExtractor: Core class for extracting and managing learnings
    Learning: Data class representing a single learning
    Pattern: Data class representing a recurring pattern

Usage:
    from extraction.learning_extractor import LearningExtractor

    extractor = LearningExtractor()

    # Process single run
    new_learnings = extractor.process_run(Path("/path/to/run-0001"))

    # Backfill all runs
    extractor.backfill(Path("/path/to/runs"))

    # Health check
    results = extractor.health_check()
"""

from .learning_extractor import LearningExtractor, Learning, Pattern

__all__ = ['LearningExtractor', 'Learning', 'Pattern']
