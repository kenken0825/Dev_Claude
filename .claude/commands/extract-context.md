# /extract-context

Extract hierarchical context from sources and generate YAML documentation.

## Usage

```
/extract-context [sources...]
```

## Arguments

- `sources` - One or more URLs, file paths, or text snippets to extract context from

## Description

This command uses the YAML Context Engineering Agent to:

1. Analyze the provided sources
2. Extract hierarchical heading structures (L1, L2, L3)
3. Generate YAML frontmatter with metadata
4. Create organized context files in Markdown format
5. Save files to the `generated_contexts` directory

## Examples

```
/extract-context https://docs.example.com/api
/extract-context docs/*.md
/extract-context "Raw text to analyze"
```

## Implementation

When invoked with `$ARGUMENTS`, the command will:

1. Parse the arguments to identify source types
2. Initialize the MCP server connection
3. Call the appropriate extraction tools
4. Generate YAML-formatted output files
5. Create an index of extracted contexts

The extracted contexts will be saved with:
- YAML frontmatter containing metadata
- Hierarchically organized content
- Related source links
- Quality metrics