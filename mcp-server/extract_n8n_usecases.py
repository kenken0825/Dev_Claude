#!/usr/bin/env python3
"""
n8n Use Cases Deep Extraction Script
Extracts complete workflow patterns and node mappings for automatic workflow generation
Target: L4 depth analysis of all n8n use cases
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


class N8nUseCaseExtractor:
    """Deep extractor for n8n use cases and workflow patterns."""
    
    def __init__(self):
        self.base_url = "https://n8n.io"
        self.visited_urls = set()
        self.use_cases = {}
        self.workflow_patterns = []
        self.node_mappings = {}
        self.max_depth = 4
        
    async def extract_use_case(self, server: YamlContextServer, url: str, depth: int = 1) -> Dict[str, Any]:
        """Extract use case details and workflow patterns."""
        
        if depth > self.max_depth or url in self.visited_urls:
            return {}
            
        self.visited_urls.add(url)
        console.info(f"[L{depth}] Extracting use case: {url}")
        
        # Fetch content
        results = await server.web_fetcher.fetch([url])
        if not results or not results[0]["success"]:
            return {}
            
        result = results[0]
        
        # Extract structure
        structure = await server.structure_extractor.extract(result["content"])
        
        # Parse use case type from URL
        use_case_type = self._parse_use_case_type(url)
        
        # Build use case data
        use_case = {
            "url": url,
            "type": use_case_type,
            "title": result.get("title", ""),
            "level": depth,
            "metadata": {
                "confidence": structure.get("confidence_score", 0.0),
                "total_headings": structure.get("total_headings", 0),
                "hierarchy_levels": structure.get("hierarchy_levels", [])
            },
            "workflow_components": {
                "triggers": [],
                "nodes": [],
                "actions": [],
                "integrations": [],
                "patterns": []
            },
            "content_analysis": {
                "key_features": [],
                "benefits": [],
                "use_cases": [],
                "examples": []
            },
            "children": []
        }
        
        # Extract workflow components from content
        content = result.get("content", "")
        use_case["workflow_components"] = self._extract_workflow_components(content)
        
        # Extract child pages for deeper analysis
        if depth < self.max_depth:
            extracted_urls = result.get("extracted_urls", [])
            
            # Filter for relevant sub-pages
            relevant_urls = [
                u for u in extracted_urls 
                if u.startswith(self.base_url) and 
                   any(pattern in u for pattern in [
                       "/workflows/", "/templates/", "/integrations/",
                       "/docs/", "/examples/", "/tutorials/"
                   ])
            ]
            
            # Process child URLs (limit to prevent explosion)
            for child_url in relevant_urls[:3]:
                if child_url not in self.visited_urls:
                    await asyncio.sleep(1)  # Rate limiting
                    child_data = await self.extract_use_case(server, child_url, depth + 1)
                    if child_data:
                        use_case["children"].append(child_data)
        
        return use_case
    
    def _parse_use_case_type(self, url: str) -> str:
        """Parse use case type from URL."""
        if "/ai-agents/" in url:
            return "AI_AGENTS"
        elif "/itops/" in url:
            return "IT_OPERATIONS"
        elif "/secops/" in url:
            return "SECURITY_OPERATIONS"
        elif "/embed/" in url:
            return "EMBEDDED_WORKFLOWS"
        elif "/lead-management/" in url:
            return "LEAD_MANAGEMENT"
        elif "/crm/" in url:
            return "CRM_AUTOMATION"
        elif "/integrations/" in url:
            return "INTEGRATIONS"
        elif "/saas/" in url:
            return "SAAS_AUTOMATION"
        else:
            return "GENERAL"
    
    def _extract_workflow_components(self, content: str) -> Dict[str, List[str]]:
        """Extract workflow components from content."""
        components = {
            "triggers": [],
            "nodes": [],
            "actions": [],
            "integrations": [],
            "patterns": []
        }
        
        # Common n8n triggers
        trigger_keywords = [
            "webhook", "schedule", "cron", "manual", "trigger",
            "event", "change", "update", "create", "delete",
            "email received", "form submission", "api call"
        ]
        
        # Common n8n nodes
        node_keywords = [
            "http request", "function", "set", "if", "switch",
            "merge", "split", "loop", "wait", "code",
            "database", "spreadsheet", "email", "slack",
            "transform", "filter", "aggregate", "format"
        ]
        
        # Common actions
        action_keywords = [
            "send", "create", "update", "delete", "fetch",
            "process", "analyze", "generate", "notify",
            "sync", "validate", "enrich", "route"
        ]
        
        # Common integrations
        integration_keywords = [
            "slack", "gmail", "google sheets", "notion",
            "airtable", "hubspot", "salesforce", "jira",
            "github", "gitlab", "discord", "telegram",
            "openai", "anthropic", "mysql", "postgres"
        ]
        
        # Extract based on keywords (simplified - real implementation would use NLP)
        content_lower = content.lower()
        
        for keyword in trigger_keywords:
            if keyword in content_lower:
                components["triggers"].append(keyword)
        
        for keyword in node_keywords:
            if keyword in content_lower:
                components["nodes"].append(keyword)
        
        for keyword in action_keywords:
            if keyword in content_lower:
                components["actions"].append(keyword)
        
        for keyword in integration_keywords:
            if keyword in content_lower:
                components["integrations"].append(keyword)
        
        # Identify workflow patterns
        if "ai" in content_lower and "agent" in content_lower:
            components["patterns"].append("ai_agent_workflow")
        if "etl" in content_lower or "data pipeline" in content_lower:
            components["patterns"].append("etl_pipeline")
        if "notification" in content_lower:
            components["patterns"].append("notification_workflow")
        if "approval" in content_lower:
            components["patterns"].append("approval_workflow")
        if "sync" in content_lower:
            components["patterns"].append("data_sync_workflow")
        
        return components
    
    def generate_workflow_dsl(self, use_cases: List[Dict[str, Any]]) -> str:
        """Generate DSL for automatic workflow creation."""
        
        dsl = """# n8n Workflow Automation DSL
# Generated: """ + datetime.utcnow().isoformat() + """Z
# Purpose: Automatic workflow generation from use case patterns

@WorkflowCatalog {
  @name: "n8n Use Case Patterns"
  @version: "1.0.0"
  @generator: "YAML Context Engineering Agent"
  
"""
        
        for use_case in use_cases:
            dsl += self._generate_use_case_dsl(use_case, 1)
            dsl += "\n"
        
        dsl += """
  @WorkflowPatterns {
"""
        
        # Generate reusable patterns
        patterns = self._extract_common_patterns(use_cases)
        for pattern_name, pattern_def in patterns.items():
            dsl += f"""
    Pattern "{pattern_name}" {{
      @triggers: {pattern_def.get('triggers', [])}
      @nodes: {pattern_def.get('nodes', [])}
      @actions: {pattern_def.get('actions', [])}
      @integrations: {pattern_def.get('integrations', [])}
    }}
"""
        
        dsl += """  }
  
  @NodeCatalog {
"""
        
        # Generate node catalog
        all_nodes = set()
        for use_case in use_cases:
            all_nodes.update(use_case.get('workflow_components', {}).get('nodes', []))
        
        for node in sorted(all_nodes):
            dsl += f"""    Node "{node}" {{
      @type: "processing"
      @category: "core"
      @inputs: ["data"]
      @outputs: ["processed_data"]
      @configuration: {{}}
    }}
"""
        
        dsl += """  }
}
"""
        
        return dsl
    
    def _generate_use_case_dsl(self, use_case: Dict[str, Any], indent: int = 0) -> str:
        """Generate DSL for a single use case."""
        
        prefix = "  " * indent
        dsl = f"""{prefix}UseCase {{
{prefix}  @type: "{use_case.get('type', 'GENERAL')}"
{prefix}  @url: "{use_case.get('url', '')}"
{prefix}  @title: "{use_case.get('title', '')}"
{prefix}  @level: L{use_case.get('level', 1)}
{prefix}  
{prefix}  @workflow {{
{prefix}    @triggers: {use_case.get('workflow_components', {}).get('triggers', [])}
{prefix}    @nodes: {use_case.get('workflow_components', {}).get('nodes', [])}
{prefix}    @actions: {use_case.get('workflow_components', {}).get('actions', [])}
{prefix}    @integrations: {use_case.get('workflow_components', {}).get('integrations', [])}
{prefix}    @patterns: {use_case.get('workflow_components', {}).get('patterns', [])}
{prefix}  }}
"""
        
        if use_case.get('children'):
            dsl += f"{prefix}  @children {{\n"
            for child in use_case['children']:
                dsl += self._generate_use_case_dsl(child, indent + 2)
            dsl += f"{prefix}  }}\n"
        
        dsl += f"{prefix}}}\n"
        
        return dsl
    
    def _extract_common_patterns(self, use_cases: List[Dict[str, Any]]) -> Dict[str, Dict]:
        """Extract common workflow patterns from use cases."""
        
        patterns = {}
        
        # AI Agent Pattern
        patterns["ai_agent"] = {
            "triggers": ["webhook", "manual", "schedule"],
            "nodes": ["http request", "function", "if", "set"],
            "actions": ["generate", "analyze", "process"],
            "integrations": ["openai", "anthropic", "slack"]
        }
        
        # Data Pipeline Pattern
        patterns["data_pipeline"] = {
            "triggers": ["schedule", "webhook"],
            "nodes": ["database", "transform", "filter", "aggregate"],
            "actions": ["fetch", "process", "sync", "update"],
            "integrations": ["mysql", "postgres", "google sheets"]
        }
        
        # Notification Pattern
        patterns["notification"] = {
            "triggers": ["event", "change", "webhook"],
            "nodes": ["if", "format", "set"],
            "actions": ["send", "notify"],
            "integrations": ["slack", "email", "discord", "telegram"]
        }
        
        # Approval Workflow Pattern
        patterns["approval_workflow"] = {
            "triggers": ["form submission", "webhook"],
            "nodes": ["wait", "if", "switch", "merge"],
            "actions": ["send", "update", "notify"],
            "integrations": ["email", "slack", "jira"]
        }
        
        return patterns


async def main():
    """Main extraction function."""
    
    # Setup
    setup_logging("INFO", structured=False)
    config = Config.from_env()
    
    # Create n8n context directory
    n8n_dir = Path("contexts/n8n-usecases")
    n8n_dir.mkdir(parents=True, exist_ok=True)
    (n8n_dir / "raw").mkdir(exist_ok=True)
    (n8n_dir / "dsl").mkdir(exist_ok=True)
    (n8n_dir / "workflows").mkdir(exist_ok=True)
    
    config.output.output_base_directory = n8n_dir
    config.crawling.max_crawl_depth = 4
    
    server = YamlContextServer(config)
    extractor = N8nUseCaseExtractor()
    
    try:
        # Target URLs
        target_urls = [
            "https://n8n.io/ai-agents/",
            "https://n8n.io/itops/",
            "https://n8n.io/secops/",
            "https://n8n.io/embed/",
            "https://n8n.io/automate-lead-management/",
            "https://n8n.io/supercharge-your-crm/",
            "https://n8n.io/limitless-integrations/",
            "https://n8n.io/saas/"
        ]
        
        console.info("🚀 Starting deep extraction of n8n use cases...")
        console.info(f"Target depth: L1-L4")
        console.info(f"Processing {len(target_urls)} use case categories")
        
        # Extract all use cases
        all_use_cases = []
        
        for url in target_urls:
            console.info(f"\n📊 Processing use case: {url}")
            use_case = await extractor.extract_use_case(server, url)
            if use_case:
                all_use_cases.append(use_case)
        
        console.success(f"✅ Extracted {len(extractor.visited_urls)} unique URLs")
        
        # Generate DSL
        console.info("\n📝 Generating Workflow Automation DSL...")
        dsl_content = extractor.generate_workflow_dsl(all_use_cases)
        
        # Save DSL
        dsl_path = n8n_dir / "dsl" / "n8n_workflow_automation.dsl"
        dsl_path.write_text(dsl_content, encoding='utf-8')
        console.success(f"✅ DSL saved to: {dsl_path}")
        
        # Generate comprehensive catalog
        console.info("\n📚 Generating comprehensive use case catalog...")
        
        catalog_content = """---
title: n8n Complete Use Case Catalog
description: Comprehensive workflow patterns for automatic generation
generated: """ + datetime.utcnow().isoformat() + """Z
total_use_cases: """ + str(len(all_use_cases)) + """
total_urls: """ + str(len(extractor.visited_urls)) + """
max_depth: 4
purpose: Automatic workflow generation foundation
---

# n8n Complete Use Case Catalog

## 🎯 Purpose
This catalog serves as the foundation for automatic n8n workflow generation,
containing all use case patterns, node mappings, and workflow templates.

## 📊 Coverage Statistics

| Metric | Value |
|--------|-------|
| **Use Case Categories** | """ + str(len(all_use_cases)) + """ |
| **Total URLs Analyzed** | """ + str(len(extractor.visited_urls)) + """ |
| **Maximum Depth** | L4 |
| **Workflow Patterns** | Multiple |

## 🔧 Use Case Categories

"""
        
        for i, use_case in enumerate(all_use_cases, 1):
            catalog_content += f"""
### {i}. {use_case.get('title', 'Untitled')}
- **Type**: {use_case.get('type', 'GENERAL')}
- **URL**: {use_case.get('url', '')}
- **Depth**: L{use_case.get('level', 1)}

#### Workflow Components
- **Triggers**: {', '.join(use_case.get('workflow_components', {}).get('triggers', [])) or 'None detected'}
- **Nodes**: {', '.join(use_case.get('workflow_components', {}).get('nodes', [])) or 'None detected'}
- **Actions**: {', '.join(use_case.get('workflow_components', {}).get('actions', [])) or 'None detected'}
- **Integrations**: {', '.join(use_case.get('workflow_components', {}).get('integrations', [])) or 'None detected'}
- **Patterns**: {', '.join(use_case.get('workflow_components', {}).get('patterns', [])) or 'None detected'}
"""
        
        catalog_content += """

## 🔄 Workflow Patterns

### AI Agent Workflow
```yaml
trigger: [webhook, manual, schedule]
nodes: [http_request, function, if, set]
actions: [generate, analyze, process]
integrations: [openai, anthropic, slack]
```

### Data Pipeline
```yaml
trigger: [schedule, webhook]
nodes: [database, transform, filter, aggregate]
actions: [fetch, process, sync, update]
integrations: [mysql, postgres, google_sheets]
```

### Notification Workflow
```yaml
trigger: [event, change, webhook]
nodes: [if, format, set]
actions: [send, notify]
integrations: [slack, email, discord, telegram]
```

### Approval Workflow
```yaml
trigger: [form_submission, webhook]
nodes: [wait, if, switch, merge]
actions: [send, update, notify]
integrations: [email, slack, jira]
```

## 🚀 Automatic Workflow Generation

### DSL Structure
```dsl
UseCase {
  @type: "USE_CASE_TYPE"
  @workflow {
    @triggers: []
    @nodes: []
    @actions: []
    @integrations: []
    @patterns: []
  }
}
```

### Generation Process
1. Select use case type
2. Choose workflow pattern
3. Configure triggers
4. Add required nodes
5. Set up integrations
6. Configure actions
7. Generate workflow JSON

## 📋 Node Catalog

### Core Nodes
- **HTTP Request**: API calls and webhooks
- **Function**: Custom JavaScript code
- **If**: Conditional branching
- **Switch**: Multi-path routing
- **Set**: Variable assignment
- **Merge**: Combine data streams
- **Split**: Divide data streams
- **Loop**: Iterate over items
- **Wait**: Delay execution

### Integration Nodes
- **Slack**: Messaging and notifications
- **Email**: Send and receive emails
- **Database**: SQL operations
- **Google Sheets**: Spreadsheet operations
- **OpenAI**: AI text generation
- **GitHub**: Repository operations
- **Jira**: Issue tracking
- **HubSpot**: CRM operations

## 🎯 Implementation Guide

### Step 1: Analyze Requirements
- Identify use case type
- Determine required integrations
- Define trigger conditions

### Step 2: Select Pattern
- Choose base workflow pattern
- Customize for specific needs
- Add error handling

### Step 3: Configure Nodes
- Set up trigger node
- Add processing nodes
- Configure integration nodes
- Add output nodes

### Step 4: Test and Deploy
- Test with sample data
- Validate error handling
- Deploy to production

---

*Generated by YAML Context Engineering Agent for n8n Workflow Automation*
"""
        
        # Save catalog
        catalog_path = n8n_dir / "n8n_use_case_catalog.md"
        catalog_path.write_text(catalog_content, encoding='utf-8')
        console.success(f"✅ Catalog saved to: {catalog_path}")
        
        # Save JSON structure
        json_path = n8n_dir / "raw" / "n8n_use_cases.json"
        json_path.write_text(
            json.dumps(all_use_cases, indent=2, ensure_ascii=False),
            encoding='utf-8'
        )
        console.success(f"✅ JSON structure saved to: {json_path}")
        
        # Generate manifest
        manifest = {
            "context_name": "n8n Use Cases",
            "version": "1.0.0",
            "extraction_date": datetime.utcnow().isoformat() + "Z",
            "purpose": "Automatic workflow generation foundation",
            "statistics": {
                "use_case_categories": len(all_use_cases),
                "total_urls": len(extractor.visited_urls),
                "max_depth": 4
            },
            "files": {
                "dsl": ["n8n_workflow_automation.dsl"],
                "catalog": ["n8n_use_case_catalog.md"],
                "raw": ["n8n_use_cases.json"]
            }
        }
        
        manifest_path = n8n_dir / "manifest.yaml"
        import yaml
        manifest_path.write_text(
            yaml.dump(manifest, default_flow_style=False),
            encoding='utf-8'
        )
        console.success(f"✅ Manifest saved to: {manifest_path}")
        
        # Summary
        console.info("\n" + "="*50)
        console.success("📊 n8n Use Case Extraction Complete!")
        console.info(f"  - URLs processed: {len(extractor.visited_urls)}")
        console.info(f"  - Use case categories: {len(all_use_cases)}")
        console.info(f"  - Files generated:")
        console.info(f"    • DSL: {dsl_path.name}")
        console.info(f"    • Catalog: {catalog_path.name}")
        console.info(f"    • JSON: {json_path.name}")
        console.info(f"    • Manifest: {manifest_path.name}")
        
    except Exception as e:
        console.error(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await server.web_fetcher.close()


if __name__ == "__main__":
    asyncio.run(main())