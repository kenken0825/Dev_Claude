# /generate-agent

Create specialized sub-agent for context extraction.

## Usage

```
/generate-agent [specialization]
```

## Arguments

- `specialization` - Type of specialized agent to create (e.g., "api-docs", "tutorial", "technical-spec")

## Description

This command generates a new specialized sub-agent tailored for specific types of context extraction:

1. **api-docs** - Optimized for API documentation extraction
2. **tutorial** - Focused on tutorial and guide content
3. **technical-spec** - Specialized for technical specifications
4. **knowledge-base** - Designed for knowledge base articles
5. **custom** - Create a custom agent with user-defined parameters

## Generated Files

```
.claude/agents/
└── [specialization]-agent.md
```

## Agent Template

Each generated agent includes:
- Custom system prompt
- Specialized tool permissions
- Extraction strategies
- Output formatting rules
- Quality criteria

## Examples

```
/generate-agent api-docs
/generate-agent tutorial
/generate-agent custom "Legal document analyzer"
```

## Implementation

When invoked with `$ARGUMENTS`, the command will:

1. Parse the specialization type
2. Load appropriate agent template
3. Customize extraction parameters
4. Generate agent configuration file
5. Update settings.json to register the agent
6. Provide usage instructions

The generated agent will be immediately available for use in context extraction tasks.