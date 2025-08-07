"""CLI interface for YAML Context Engineering."""

import asyncio
import sys
import click
from pathlib import Path
from typing import Optional

from .server import YamlContextServer
from .config import Config
from .utils.logging import console, setup_logging


@click.group()
@click.option('--verbose', is_flag=True, help='Enable verbose output')
@click.pass_context
def cli(ctx: click.Context, verbose: bool) -> None:
    """YAML Context Engineering CLI."""
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level, structured=False)
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = verbose


@cli.command()
@click.argument('sources', nargs=-1, required=True)
@click.option('--output-dir', '-o', type=Path, help='Output directory')
@click.option('--depth', '-d', type=int, default=2, help='Crawl depth')
@click.option('--format', '-f', type=click.Choice(['yaml', 'markdown', 'json']), default='markdown', help='Output format')
async def extract(sources: tuple, output_dir: Optional[Path], depth: int, format: str) -> None:
    """Extract context from multiple sources (URLs, files, or text)."""
    config = Config.from_env()
    
    if output_dir:
        config.output.output_base_directory = output_dir
    if depth:
        config.crawling.max_crawl_depth = depth
    
    server = YamlContextServer(config)
    
    # Process multiple sources
    urls = []
    files = []
    texts = []
    
    for source in sources:
        if source.startswith('http://') or source.startswith('https://'):
            urls.append(source)
        elif Path(source).exists():
            files.append(Path(source))
        else:
            texts.append(source)
    
    try:
        all_results = []
        
        # Process URLs
        if urls:
            for url in urls:
                console.info(f"Fetching content from {url}...")
                results = await server.web_fetcher.fetch([url])
                
                if results and results[0]["success"]:
                    all_results.append((url, results[0]))
                else:
                    console.error(f"Failed to fetch {url}")
        
        # Process files
        if files:
            for file in files:
                console.info(f"Reading file {file}...")
                with open(file, 'r', encoding='utf-8') as f:
                    content = f.read()
                all_results.append((str(file), {
                    "content": content,
                    "title": file.stem,
                    "success": True,
                    "language": "unknown"
                }))
        
        # Process text inputs
        if texts:
            for i, text in enumerate(texts):
                console.info(f"Processing text input {i+1}...")
                all_results.append((f"text_{i+1}", {
                    "content": text,
                    "title": f"Text Input {i+1}",
                    "success": True,
                    "language": "unknown"
                }))
        
        # Process all results
        for source_name, result in all_results:
            if not result["success"]:
                continue
            
            # Extract structure
            console.info(f"Extracting hierarchical structure for {source_name}...")
            structure = await server.structure_extractor.extract(result["content"])
            
            # Save to file
            console.info(f"Generating {format.upper()} documentation...")
            
            # Generate filename
            if source_name.startswith('http'):
                filename = Path(source_name).name or "extracted"
            elif source_name.startswith('text_'):
                filename = source_name
            else:
                filename = Path(source_name).stem
            
            # Create output based on format
            if format == 'markdown':
                await server.file_manager.execute(
                    "write_file",
                    f"{filename}.md",
                    {
                        "title": result.get("title", "Extracted Content"),
                        "source_url": source_name,
                        "language": result.get("language", "unknown"),
                        "body": result["content"],
                        "hierarchy_levels": structure.get("hierarchy_levels", [])
                    }
                )
                console.success(f"✅ Context extracted to: {config.output.output_base_directory}/{filename}.md")
            elif format == 'yaml':
                import yaml
                # Limit structure depth to avoid recursion issues
                structured_headings = structure.get("structured_headings", [])
                # Simple serialization - convert to basic dict without deep recursion
                simplified_structure = []
                for heading in structured_headings[:10]:  # Limit to first 10 headings
                    simplified_structure.append({
                        "text": heading.get("text", ""),
                        "level": heading.get("level", 0)
                    })
                
                yaml_content = yaml.dump({
                    "title": result.get("title", "Extracted Content"),
                    "source_url": source_name,
                    "language": result.get("language", "unknown"),
                    "hierarchy_levels": structure.get("hierarchy_levels", []),
                    "total_headings": structure.get("total_headings", 0),
                    "confidence_score": structure.get("confidence_score", 0.0),
                    "format_detected": structure.get("format_detected", "unknown"),
                    "structure": simplified_structure
                }, default_flow_style=False, allow_unicode=True)
                
                output_path = config.output.output_base_directory / f"{filename}.yaml"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(yaml_content, encoding='utf-8')
                console.success(f"✅ Context extracted to: {output_path}")
            elif format == 'json':
                import json
                # Limit structure depth to avoid recursion issues
                structured_headings = structure.get("structured_headings", [])
                simplified_structure = []
                for heading in structured_headings[:10]:  # Limit to first 10 headings
                    simplified_structure.append({
                        "text": heading.get("text", ""),
                        "level": heading.get("level", 0)
                    })
                
                json_content = json.dumps({
                    "title": result.get("title", "Extracted Content"),
                    "source_url": source_name,
                    "language": result.get("language", "unknown"),
                    "hierarchy_levels": structure.get("hierarchy_levels", []),
                    "total_headings": structure.get("total_headings", 0),
                    "confidence_score": structure.get("confidence_score", 0.0),
                    "format_detected": structure.get("format_detected", "unknown"),
                    "structure": simplified_structure
                }, indent=2, ensure_ascii=False)
                
                output_path = config.output.output_base_directory / f"{filename}.json"
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(json_content, encoding='utf-8')
                console.success(f"✅ Context extracted to: {output_path}")
        
    except Exception as e:
        console.error(f"Error: {e}")
        sys.exit(1)
    finally:
        await server.web_fetcher.close()


@cli.command()
@click.argument('file', type=Path)
@click.option('--output-dir', '-o', type=Path, help='Output directory')
async def analyze(file: Path, output_dir: Optional[Path]) -> None:
    """Analyze local file structure."""
    if not file.exists():
        console.error(f"File not found: {file}")
        sys.exit(1)
    
    config = Config.from_env()
    if output_dir:
        config.output.output_base_directory = output_dir
    
    server = YamlContextServer(config)
    
    try:
        # Read file content
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract structure
        console.info(f"Analyzing structure of {file}...")
        structure = await server.structure_extractor.extract(content)
        
        # Display results
        console.info(f"Format detected: {structure['format_detected']}")
        console.info(f"Total headings: {structure['total_headings']}")
        console.info(f"Confidence: {structure['confidence_score']:.2f}")
        console.info(f"Hierarchy levels: {structure['hierarchy_levels']}")
        
        # Save analysis
        await server.file_manager.execute(
            "write_file",
            f"{file.stem}_analysis.md",
            {
                "title": f"Analysis of {file.name}",
                "source_url": str(file.absolute()),
                "body": generate_analysis_report(structure)
            }
        )
        
        console.success(f"✅ Analysis saved to: {config.output.output_base_directory}/{file.stem}_analysis.md")
        
    except Exception as e:
        console.error(f"Error: {e}")
        sys.exit(1)


def generate_analysis_report(structure: dict) -> str:
    """Generate markdown report from structure analysis."""
    report = f"""# Structure Analysis Report

## Summary
- **Format**: {structure['format_detected']}
- **Total Headings**: {structure['total_headings']}
- **Confidence Score**: {structure['confidence_score']:.2f}
- **Hierarchy Levels**: {', '.join(map(str, structure['hierarchy_levels']))}

## Hierarchical Structure

"""
    
    def render_heading(heading: dict, level: int = 0) -> str:
        indent = "  " * level
        output = f"{indent}- **{heading['text']}** (L{heading['level']})\n"
        if heading.get('children'):
            for child in heading['children']:
                output += render_heading(child, level + 1)
        return output
    
    for heading in structure['structured_headings']:
        report += render_heading(heading)
    
    if structure.get('extracted_entities'):
        report += "\n## Extracted Entities\n\n"
        entities = structure['extracted_entities']
        
        if entities.get('urls'):
            report += f"### URLs ({len(entities['urls'])})\n"
            for url in entities['urls'][:10]:  # First 10
                report += f"- {url}\n"
            if len(entities['urls']) > 10:
                report += f"- ... and {len(entities['urls']) - 10} more\n"
        
        if entities.get('key_terms'):
            report += f"\n### Key Terms ({len(entities['key_terms'])})\n"
            for term in entities['key_terms'][:20]:  # First 20
                report += f"- {term}\n"
    
    return report


@cli.group()
def ldd() -> None:
    """LDD (Log-Driven Development) commands."""
    pass


@ldd.command('init')
@click.option('--logs-dir', default='./logs', help='Logs directory')
@click.option('--memory-bank', default='./@memory-bank.md', help='Memory bank file path')
@click.pass_context
async def ldd_init(ctx: click.Context, logs_dir: str, memory_bank: str) -> None:
    """Initialize LDD system."""
    from .ldd import LDDConfig, LoggingEngine, MemoryBank
    
    try:
        console.info("🚀 Initializing LDD system...")
        
        # Create LDD config
        config = LDDConfig(
            logsDir=logs_dir,
            memoryBankPath=memory_bank
        )
        
        # Initialize components
        logging_engine = LoggingEngine(config)
        memory_bank_obj = MemoryBank(config)
        
        # Save config
        import json
        with open('.ldd-config.json', 'w') as f:
            json.dump({
                'logsDir': config.logsDir,
                'memoryBankPath': config.memoryBankPath,
                'templatePath': config.templatePath,
                'enableAutoLogging': config.enableAutoLogging
            }, f, indent=2)
        
        console.success("✅ LDD system initialized successfully!")
        console.info(f"  Logs directory: {logs_dir}")
        console.info(f"  Memory bank: {memory_bank}")
        
    except Exception as e:
        console.error(f"❌ Failed to initialize LDD system: {e}")
        sys.exit(1)


@ldd.command('task')
@click.argument('task_name')
@click.option('-a', '--agent', default='yaml-context-agent', help='Agent name')
@click.option('-p', '--project', help='Project name')
@click.option('-m', '--module', help='Module/component name')
@click.pass_context
async def ldd_task(ctx: click.Context, task_name: str, agent: str, 
                   project: Optional[str], module: Optional[str]) -> None:
    """Create a new task log."""
    from .ldd import LDDConfig, LoggingEngine
    import json
    
    try:
        # Load config
        if Path('.ldd-config.json').exists():
            with open('.ldd-config.json', 'r') as f:
                config_data = json.load(f)
                config = LDDConfig(**config_data)
        else:
            config = LDDConfig()
        
        logging_engine = LoggingEngine(config)
        
        # Create task
        context = {}
        if project:
            context['project'] = project
        if module:
            context['module'] = module
        
        log_entry = await logging_engine.create_task_log({
            'taskName': task_name,
            'agent': agent,
            'context': context,
            'status': 'Initiated'
        })
        
        console.success(f"✅ Task log created: {log_entry['id']}")
        console.info(f"  Task: {task_name}")
        console.info(f"  Status: {log_entry['status']}")
        console.info(f"  Agent: {log_entry['agent']}")
        
    except Exception as e:
        console.error(f"❌ Failed to create task log: {e}")
        sys.exit(1)


@ldd.command('memory')
@click.argument('description')
@click.option('-t', '--type', default='Learning', help='Entry type')
@click.option('-a', '--agent', default='yaml-context-agent', help='Agent name')
@click.option('--tags', help='Comma-separated tags')
@click.pass_context
async def ldd_memory(ctx: click.Context, description: str, type: str, 
                    agent: str, tags: Optional[str]) -> None:
    """Add entry to memory bank."""
    from .ldd import LDDConfig, MemoryBank
    import json
    
    try:
        # Load config
        if Path('.ldd-config.json').exists():
            with open('.ldd-config.json', 'r') as f:
                config_data = json.load(f)
                config = LDDConfig(**config_data)
        else:
            config = LDDConfig()
        
        memory_bank = MemoryBank(config)
        await memory_bank.initialize()
        
        # Create memory entry
        entry = await memory_bank.append_entry({
            'type': type,
            'agent': agent,
            'details': {
                'description': description,
                'insights': [],
                'impact': 'To be determined'
            },
            'tags': tags.split(',') if tags else []
        })
        
        console.success(f"✅ Memory entry added: {entry['id']}")
        console.info(f"  Type: {entry['type']}")
        console.info(f"  Agent: {entry['agent']}")
        
    except Exception as e:
        console.error(f"❌ Failed to add memory entry: {e}")
        sys.exit(1)


@cli.command('setup-project')
@click.argument('project_name')
@click.option('--template', '-t', type=click.Choice(['basic', 'advanced', 'mcp']), default='basic', help='Project template')
@click.pass_context
def setup_project(ctx: click.Context, project_name: str, template: str) -> None:
    """Initialize YAML Context Engineering project structure."""
    project_path = Path(project_name)
    
    if project_path.exists():
        console.error(f"Project {project_name} already exists!")
        sys.exit(1)
    
    try:
        console.info(f"Creating project: {project_name}...")
        
        # Create project structure
        project_path.mkdir(parents=True)
        (project_path / "generated_contexts").mkdir()
        (project_path / "logs").mkdir()
        (project_path / "templates").mkdir()
        
        # Create config file
        config_content = {
            "project_name": project_name,
            "version": "1.0.0",
            "template": template,
            "output": {
                "base_directory": "generated_contexts",
                "format": "markdown"
            },
            "crawling": {
                "max_depth": 3,
                "delay_seconds": 1.0
            }
        }
        
        import json
        with open(project_path / "config.json", 'w') as f:
            json.dump(config_content, f, indent=2)
        
        # Create README
        readme_content = f"""# {project_name}

YAML Context Engineering Project

## Setup

```bash
yaml-context extract <sources...>
```

## Configuration

Edit `config.json` to customize settings.
"""
        
        (project_path / "README.md").write_text(readme_content)
        
        console.success(f"✅ Project {project_name} created successfully!")
        console.info(f"  Directory: {project_path.absolute()}")
        console.info(f"  Template: {template}")
        
    except Exception as e:
        console.error(f"Failed to create project: {e}")
        sys.exit(1)


@cli.command('generate-agent')
@click.argument('specialization')
@click.option('--name', '-n', help='Agent name')
@click.option('--tools', '-t', multiple=True, help='Tools to include')
@click.pass_context
def generate_agent(ctx: click.Context, specialization: str, name: Optional[str], tools: tuple) -> None:
    """Create specialized sub-agent for context extraction."""
    agent_name = name or f"{specialization}-agent"
    
    try:
        console.info(f"Generating agent: {agent_name}...")
        
        # Create agent directory
        agent_dir = Path(".claude/agents")
        agent_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate agent configuration
        agent_config = f"""---
name: {agent_name}
specialization: {specialization}
tools: {list(tools) if tools else ['WebFetch', 'Read', 'Write']}
---

# {agent_name.replace('-', ' ').title()}

You are a specialized agent for {specialization}.

## Capabilities

- Extract and analyze {specialization} content
- Generate structured documentation
- Identify key patterns and relationships

## Instructions

1. Analyze provided content for {specialization}-specific patterns
2. Extract hierarchical structure
3. Generate YAML-formatted output
4. Ensure high quality and accuracy
"""
        
        agent_file = agent_dir / f"{agent_name}.md"
        agent_file.write_text(agent_config)
        
        console.success(f"✅ Agent {agent_name} created successfully!")
        console.info(f"  File: {agent_file.absolute()}")
        console.info(f"  Specialization: {specialization}")
        
    except Exception as e:
        console.error(f"Failed to generate agent: {e}")
        sys.exit(1)


def main() -> None:
    """Main entry point for CLI."""
    # Check if this is an async command
    is_async_command = False
    if len(sys.argv) > 1:
        if sys.argv[1] in ['extract', 'analyze']:
            is_async_command = True
        elif sys.argv[1] == 'ldd' and len(sys.argv) > 2:
            # LDD subcommands are also async
            is_async_command = True
    
    if is_async_command:
        # Create new event loop for async commands
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Run async commands
        try:
            loop.run_until_complete(cli.main(standalone_mode=False))
        except SystemExit:
            # Click commands can call sys.exit()
            pass
        except Exception as e:
            # Click will handle most exceptions, but catch any others
            print(f"Error: {e}")
        finally:
            loop.close()
    else:
        # Non-async commands
        cli()


if __name__ == "__main__":
    main()