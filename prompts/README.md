# RALF Prompts Directory

Store project-specific RALF prompts here.

## Usage

```bash
# Run with default prompt (blackbox5)
c

# Run with specific project prompt
c coursework

# Run with full path
c ~/.blackbox5/prompts/coursework.md
```

## Creating New Prompts

1. Create a `.md` file in this directory
2. Name it after your project (e.g., `coursework.md`)
3. Run with `c <project-name>`

## Prompt Structure

Each prompt should:
- Define the agent's purpose
- Set project-specific paths
- Reference the global BlackBox5 at `~/.blackbox5/`

## Available Prompts

- `blackbox5.md` - Default BlackBox5 system improvement
