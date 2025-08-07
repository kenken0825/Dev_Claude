#!/usr/bin/env python3
"""Test script for YAML Context Engineering extraction."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.server import YamlContextServer
from yaml_context_engineering.utils.logging import console, setup_logging


async def main():
    """Test extraction from Slack API docs."""
    
    # Setup logging
    setup_logging("INFO", structured=False)
    
    # Create config
    config = Config.from_env()
    config.output.output_base_directory = Path("my-project/generated_contexts")
    
    # Create server
    server = YamlContextServer(config)
    
    try:
        # Test URL
        url = "https://api.slack.com/docs"
        
        # Fetch content
        console.info(f"Fetching content from {url}...")
        results = await server.web_fetcher.fetch([url])
        
        if not results or not results[0]["success"]:
            console.error(f"Failed to fetch {url}")
            return
        
        result = results[0]
        console.success(f"✅ Fetched successfully")
        console.info(f"  Title: {result.get('title', 'N/A')}")
        console.info(f"  Content length: {len(result.get('content', ''))}")
        
        # Extract structure
        console.info("Extracting hierarchical structure...")
        structure = await server.structure_extractor.extract(result["content"])
        
        console.success(f"✅ Structure extracted")
        console.info(f"  Format: {structure.get('format_detected', 'unknown')}")
        console.info(f"  Total headings: {structure.get('total_headings', 0)}")
        console.info(f"  Confidence: {structure.get('confidence_score', 0.0):.2f}")
        console.info(f"  Hierarchy levels: {structure.get('hierarchy_levels', [])}")
        
        # Save to file - simple approach
        output_path = config.output.output_base_directory / "slack_api_docs.md"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create markdown content with YAML frontmatter
        content = f"""---
title: {result.get('title', 'Slack API Documentation')}
source_url: {url}
language: {result.get('language', 'en')}
extracted_by: YAML Context Engineering Agent
total_headings: {structure.get('total_headings', 0)}
confidence_score: {structure.get('confidence_score', 0.0)}
format_detected: {structure.get('format_detected', 'unknown')}
hierarchy_levels: {structure.get('hierarchy_levels', [])}
---

# {result.get('title', 'Slack API Documentation')}

## Structure Overview

- **Total Headings**: {structure.get('total_headings', 0)}
- **Confidence Score**: {structure.get('confidence_score', 0.0):.2f}
- **Format**: {structure.get('format_detected', 'unknown')}

## Extracted Headings

"""
        
        # Add headings
        structured_headings = structure.get('structured_headings', [])
        for i, heading in enumerate(structured_headings[:20]):  # First 20 headings
            level = heading.get('level', 1)
            text = heading.get('text', '')
            indent = "  " * (level - 1)
            content += f"{indent}- **L{level}**: {text}\n"
        
        if len(structured_headings) > 20:
            content += f"\n... and {len(structured_headings) - 20} more headings\n"
        
        # Add raw content snippet
        content += f"\n## Content Preview\n\n```\n{result['content'][:500]}...\n```\n"
        
        # Write file
        output_path.write_text(content, encoding='utf-8')
        console.success(f"✅ Context saved to: {output_path}")
        
        # Also save as YAML
        import yaml
        yaml_path = config.output.output_base_directory / "slack_api_docs.yaml"
        
        yaml_data = {
            "title": result.get('title', 'Slack API Documentation'),
            "source_url": url,
            "language": result.get('language', 'en'),
            "total_headings": structure.get('total_headings', 0),
            "confidence_score": structure.get('confidence_score', 0.0),
            "format_detected": structure.get('format_detected', 'unknown'),
            "hierarchy_levels": structure.get('hierarchy_levels', []),
            "headings": [
                {"level": h.get('level', 0), "text": h.get('text', '')}
                for h in structured_headings[:20]
            ]
        }
        
        yaml_content = yaml.dump(yaml_data, default_flow_style=False, allow_unicode=True)
        yaml_path.write_text(yaml_content, encoding='utf-8')
        console.success(f"✅ YAML saved to: {yaml_path}")
        
    except Exception as e:
        console.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.web_fetcher.close()


if __name__ == "__main__":
    asyncio.run(main())