#!/usr/bin/env python3
"""
Hello module - A simple greeting utility.

This module provides functions for generating personalized greetings.
Designed for extensibility and ease of use.
"""

from typing import Optional


class Greeter:
    """
    A configurable greeting generator.

    Attributes:
        default_name: The default name to use when none is provided.
        greeting_style: The style of greeting (formal, casual, excited).
    """

    def __init__(
        self,
        default_name: str = "World",
        greeting_style: str = "casual"
    ) -> None:
        """
        Initialize the Greeter.

        Args:
            default_name: Default name for greetings.
            greeting_style: Style of greeting (formal, casual, excited).

        Raises:
            ValueError: If greeting_style is not a valid style.
        """
        valid_styles = {"formal", "casual", "excited"}
        if greeting_style not in valid_styles:
            raise ValueError(
                f"Invalid style '{greeting_style}'. "
                f"Must be one of: {valid_styles}"
            )

        self.default_name = default_name
        self.greeting_style = greeting_style

    def greet(self, name: Optional[str] = None) -> str:
        """
        Generate a greeting message.

        Args:
            name: Name to greet. Uses default_name if not provided.

        Returns:
            A formatted greeting string.
        """
        target = name or self.default_name

        templates = {
            "formal": f"Hello, {target}.",
            "casual": f"Hey {target}!",
            "excited": f"Hello, {target}!!! 🎉"
        }

        return templates[self.greeting_style]

    def say_hello(self, name: Optional[str] = None) -> None:
        """
        Print a greeting to stdout.

        Args:
            name: Name to greet. Uses default_name if not provided.
        """
        print(self.greet(name))


def hello(name: Optional[str] = None) -> str:
    """
    Generate a simple greeting.

    Convenience function for quick greetings without creating a Greeter instance.

    Args:
        name: Name to greet. Defaults to "World".

    Returns:
        A greeting string.

    Example:
        >>> hello()
        'Hello, World!'
        >>> hello("Alice")
        'Hello, Alice!'
    """
    target = name or "World"
    return f"Hello, {target}!"


def main() -> None:
    """CLI entry point."""
    import argparse

    parser = argparse.ArgumentParser(description="Say hello")
    parser.add_argument(
        "--name", "-n",
        default="World",
        help="Name to greet (default: World)"
    )
    parser.add_argument(
        "--style", "-s",
        choices=["formal", "casual", "excited"],
        default="casual",
        help="Greeting style"
    )

    args = parser.parse_args()

    greeter = Greeter(default_name=args.name, greeting_style=args.style)
    greeter.say_hello()


if __name__ == "__main__":
    main()
