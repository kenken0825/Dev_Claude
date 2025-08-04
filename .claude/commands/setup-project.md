# /setup-project

Initialize YAML Context Engineering project structure.

## Usage

```
/setup-project [project-name]
```

## Arguments

- `project-name` - Name of the project to initialize (optional, defaults to current directory name)

## Description

This command sets up a complete YAML Context Engineering project with:

1. Directory structure for context extraction
2. Configuration files
3. MCP server integration
4. Claude Code hooks and settings
5. GitHub Actions workflows
6. Documentation templates

## Project Structure

```
project-name/
├── .claude/
│   ├── settings.json
│   ├── commands/
│   └── agents/
├── mcp-server/
│   ├── src/
│   ├── tests/
│   └── requirements.txt
├── generated_contexts/
│   └── .gitkeep
├── .github/
│   └── workflows/
│       ├── context-extraction.yml
│       └── auto-review.yml
├── docs/
│   ├── README.md
│   └── guides/
├── PLANNING.md
└── .gitignore
```

## Implementation

When invoked with `$ARGUMENTS`, the command will:

1. Create project directory structure
2. Initialize Git repository
3. Install MCP server dependencies
4. Configure Claude Code settings
5. Set up GitHub Actions
6. Create initial documentation
7. Generate sample configuration

The project will be ready for immediate use with context extraction capabilities.