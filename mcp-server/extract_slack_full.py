#!/usr/bin/env python3
"""
Slack API Documentation Deep Extraction Script
Extracts complete hierarchical structure up to L4 depth
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Dict, List, Any
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.server import YamlContextServer
from yaml_context_engineering.utils.logging import console, setup_logging


class SlackAPIExtractor:
    """Deep extractor for Slack API documentation."""
    
    def __init__(self):
        self.base_url = "https://api.slack.com"
        self.visited_urls = set()
        self.hierarchy = {}
        self.max_depth = 4
        
    async def extract_deep_structure(self, server: YamlContextServer, url: str, depth: int = 1) -> Dict[str, Any]:
        """Extract deep hierarchical structure from URL."""
        
        if depth > self.max_depth or url in self.visited_urls:
            return {}
            
        self.visited_urls.add(url)
        
        console.info(f"[L{depth}] Extracting: {url}")
        
        # Fetch content
        results = await server.web_fetcher.fetch([url])
        if not results or not results[0]["success"]:
            return {}
            
        result = results[0]
        
        # Extract structure
        structure = await server.structure_extractor.extract(result["content"])
        
        # Build hierarchical data
        node = {
            "url": url,
            "title": result.get("title", ""),
            "level": depth,
            "total_headings": structure.get("total_headings", 0),
            "headings": [],
            "children": [],
            "content_preview": result["content"][:500] if result.get("content") else "",
            "metadata": {
                "confidence": structure.get("confidence_score", 0.0),
                "format": structure.get("format_detected", "unknown"),
                "hierarchy_levels": structure.get("hierarchy_levels", [])
            }
        }
        
        # Process headings
        structured_headings = structure.get("structured_headings", [])
        for heading in structured_headings[:20]:  # Limit to prevent explosion
            heading_data = {
                "text": heading.get("text", ""),
                "level": heading.get("level", 0),
                "type": f"L{heading.get('level', 0)}"
            }
            node["headings"].append(heading_data)
        
        # Extract child URLs if we haven't reached max depth
        if depth < self.max_depth:
            # Extract URLs from content
            extracted_urls = result.get("extracted_urls", [])
            
            # Filter for API documentation URLs
            api_urls = [
                u for u in extracted_urls 
                if u.startswith(self.base_url) and 
                   ("/docs" in u or "/methods" in u or "/reference" in u)
            ]
            
            # Process child URLs (limit to prevent explosion)
            for child_url in api_urls[:5]:
                if child_url not in self.visited_urls:
                    await asyncio.sleep(1)  # Rate limiting
                    child_node = await self.extract_deep_structure(server, child_url, depth + 1)
                    if child_node:
                        node["children"].append(child_node)
        
        return node
        
    def generate_dsl(self, hierarchy: Dict[str, Any], indent: int = 0) -> str:
        """Generate DSL representation of hierarchy."""
        
        dsl = ""
        prefix = "  " * indent
        
        # Node definition
        dsl += f"{prefix}Node {{\n"
        dsl += f"{prefix}  @type: \"documentation\"\n"
        dsl += f"{prefix}  @level: L{hierarchy.get('level', 1)}\n"
        dsl += f"{prefix}  @url: \"{hierarchy.get('url', '')}\"\n"
        dsl += f"{prefix}  @title: \"{hierarchy.get('title', '')}\"\n"
        
        # Metadata
        metadata = hierarchy.get("metadata", {})
        dsl += f"{prefix}  @metadata {{\n"
        dsl += f"{prefix}    confidence: {metadata.get('confidence', 0.0):.2f}\n"
        dsl += f"{prefix}    format: \"{metadata.get('format', 'unknown')}\"\n"
        dsl += f"{prefix}    hierarchy_levels: {metadata.get('hierarchy_levels', [])}\n"
        dsl += f"{prefix}  }}\n"
        
        # Headings
        if hierarchy.get("headings"):
            dsl += f"{prefix}  @headings {{\n"
            for heading in hierarchy["headings"]:
                dsl += f"{prefix}    {heading['type']}: \"{heading['text']}\"\n"
            dsl += f"{prefix}  }}\n"
        
        # Children
        if hierarchy.get("children"):
            dsl += f"{prefix}  @children {{\n"
            for child in hierarchy["children"]:
                dsl += self.generate_dsl(child, indent + 2)
            dsl += f"{prefix}  }}\n"
        
        dsl += f"{prefix}}}\n"
        
        return dsl


async def main():
    """Main extraction function."""
    
    # Setup
    setup_logging("INFO", structured=False)
    config = Config.from_env()
    config.output.output_base_directory = Path("my-project/generated_contexts")
    config.crawling.max_crawl_depth = 4
    
    server = YamlContextServer(config)
    extractor = SlackAPIExtractor()
    
    try:
        # Primary documentation URLs
        primary_urls = [
            "https://api.slack.com/docs",
            "https://api.slack.com/methods",
            "https://api.slack.com/reference",
            "https://api.slack.com/apis",
            "https://api.slack.com/events-api",
            "https://api.slack.com/rtm",
            "https://api.slack.com/scopes",
            "https://api.slack.com/authentication",
            "https://api.slack.com/apps",
            "https://api.slack.com/tools"
        ]
        
        console.info("🚀 Starting deep extraction of Slack API documentation...")
        console.info(f"Target depth: L1-L4")
        console.info(f"Processing {len(primary_urls)} primary URLs")
        
        # Extract hierarchy
        full_hierarchy = {
            "root": "Slack API Documentation",
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "max_depth": 4,
            "sections": []
        }
        
        for url in primary_urls:
            console.info(f"\n📄 Processing section: {url}")
            section = await extractor.extract_deep_structure(server, url)
            if section:
                full_hierarchy["sections"].append(section)
        
        console.success(f"✅ Extracted {len(extractor.visited_urls)} unique URLs")
        
        # Generate DSL
        console.info("\n📝 Generating DSL representation...")
        
        dsl_content = """# Slack API Documentation Structure DSL
# Generated: """ + datetime.utcnow().isoformat() + """Z
# Depth: L1-L4
# Total URLs Processed: """ + str(len(extractor.visited_urls)) + """

@Document {
  @name: "Slack API Complete Manual"
  @version: "1.0.0"
  @generator: "YAML Context Engineering Agent"
  
"""
        
        for section in full_hierarchy["sections"]:
            dsl_content += extractor.generate_dsl(section, 1)
            dsl_content += "\n"
        
        dsl_content += "}\n"
        
        # Save DSL
        dsl_path = config.output.output_base_directory / "slack_api_dsl.txt"
        dsl_path.write_text(dsl_content, encoding='utf-8')
        console.success(f"✅ DSL saved to: {dsl_path}")
        
        # Generate structured manual
        console.info("\n📚 Generating complete manual...")
        
        manual_content = """---
title: Slack API Complete Manual
description: Comprehensive documentation structure with L1-L4 hierarchy
generated: """ + datetime.utcnow().isoformat() + """Z
total_sections: """ + str(len(full_hierarchy["sections"])) + """
total_urls: """ + str(len(extractor.visited_urls)) + """
max_depth: 4
---

# Slack API Complete Manual

## Executive Summary

This manual provides a complete hierarchical structure of the Slack API documentation,
organized in a DSL (Domain Specific Language) format with depth up to L4.

## Document Structure

### Processing Statistics
- **Total URLs Processed**: """ + str(len(extractor.visited_urls)) + """
- **Maximum Depth**: L4
- **Primary Sections**: """ + str(len(full_hierarchy["sections"])) + """

## Hierarchical Structure

"""
        
        def format_hierarchy(node, level=1):
            indent = "  " * (level - 1)
            output = f"{indent}- **L{node.get('level', 1)}**: [{node.get('title', 'Untitled')}]({node.get('url', '#')})\n"
            
            # Add headings
            for heading in node.get('headings', [])[:5]:
                h_indent = "  " * level
                output += f"{h_indent}- {heading['type']}: {heading['text']}\n"
            
            # Add children
            for child in node.get('children', []):
                output += format_hierarchy(child, level + 1)
            
            return output
        
        for i, section in enumerate(full_hierarchy["sections"], 1):
            manual_content += f"\n### Section {i}: {section.get('title', 'Untitled')}\n\n"
            manual_content += format_hierarchy(section)
        
        # Add DSL reference
        manual_content += """

## DSL Format Reference

The documentation structure is represented in a custom DSL format with the following syntax:

```dsl
Node {
  @type: "documentation"
  @level: L[1-4]
  @url: "https://..."
  @title: "Page Title"
  @metadata {
    confidence: 0.00
    format: "markdown|html"
    hierarchy_levels: [1, 2, 3, 4]
  }
  @headings {
    L1: "Main Heading"
    L2: "Subheading"
    ...
  }
  @children {
    Node { ... }
  }
}
```

## API Coverage

### Core APIs
- Web API Methods
- Events API
- RTM API
- SCIM API

### Authentication & Security
- OAuth 2.0
- Token Types
- Scopes & Permissions

### Development Tools
- SDKs & Libraries
- Bolt Framework
- Block Kit Builder
- API Tester

## Usage Guidelines

1. Navigate through the hierarchy using the L1-L4 depth indicators
2. Each node contains metadata about confidence and format
3. Child nodes represent deeper documentation pages
4. DSL format can be parsed programmatically for tooling

---

*Generated by YAML Context Engineering Agent*
"""
        
        # Save manual
        manual_path = config.output.output_base_directory / "slack_api_manual.md"
        manual_path.write_text(manual_content, encoding='utf-8')
        console.success(f"✅ Manual saved to: {manual_path}")
        
        # Save JSON structure
        json_path = config.output.output_base_directory / "slack_api_structure.json"
        json_path.write_text(
            json.dumps(full_hierarchy, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        console.success(f"✅ JSON structure saved to: {json_path}")
        
        # Summary
        console.info("\n" + "="*50)
        console.success("📊 Extraction Complete!")
        console.info(f"  - URLs processed: {len(extractor.visited_urls)}")
        console.info(f"  - Primary sections: {len(full_hierarchy['sections'])}")
        console.info(f"  - Files generated:")
        console.info(f"    • DSL: {dsl_path.name}")
        console.info(f"    • Manual: {manual_path.name}")
        console.info(f"    • JSON: {json_path.name}")
        
    except Exception as e:
        console.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.web_fetcher.close()


if __name__ == "__main__":
    asyncio.run(main())