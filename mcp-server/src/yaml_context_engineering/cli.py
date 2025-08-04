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
def cli(verbose: bool) -> None:
    """YAML Context Engineering CLI."""
    log_level = "DEBUG" if verbose else "INFO"
    setup_logging(log_level, structured=False)


@cli.command()
@click.argument('url')
@click.option('--output-dir', '-o', type=Path, help='Output directory')
@click.option('--depth', '-d', type=int, default=2, help='Crawl depth')
async def extract(url: str, output_dir: Optional[Path], depth: int) -> None:
    """Extract context from URL."""
    config = Config.from_env()
    
    if output_dir:
        config.output.output_base_directory = output_dir
    if depth:
        config.crawling.max_crawl_depth = depth
    
    server = YamlContextServer(config)
    
    try:
        # Use the web content fetcher
        console.info(f"Fetching content from {url}...")
        results = await server.web_fetcher.fetch([url])
        
        if not results or not results[0]["success"]:
            console.error(f"Failed to fetch {url}")
            sys.exit(1)
        
        # Extract structure
        console.info("Extracting hierarchical structure...")
        structure = await server.structure_extractor.extract(results[0]["content"])
        
        # Save to file
        console.info("Generating YAML documentation...")
        filename = Path(url).name or "extracted"
        await server.file_manager.execute(
            "write_file",
            f"{filename}.md",
            {
                "title": results[0].get("title", "Extracted Content"),
                "source_url": url,
                "language": results[0].get("language", "unknown"),
                "body": results[0]["content"],
                "hierarchy_levels": structure.get("hierarchy_levels", [])
            }
        )
        
        console.success(f"✅ Context extracted to: {config.output.output_base_directory}/{filename}.md")
        
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


def main() -> None:
    """Main entry point for CLI."""
    # Handle async commands
    if len(sys.argv) > 1 and sys.argv[1] in ['extract', 'analyze']:
        # Create new event loop for async commands
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        # Modify argv to work with click's async handling
        async def run():
            await cli.main(standalone_mode=False)
        
        try:
            loop.run_until_complete(run())
        except Exception:
            # Click will handle the exception
            pass
        finally:
            loop.close()
    else:
        # Non-async commands
        cli()


if __name__ == "__main__":
    main()