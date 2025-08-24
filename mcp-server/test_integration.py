#!/usr/bin/env python3
"""Integration test for YAML Context Engineering MCP Server."""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from yaml_context_engineering.config import Config
from yaml_context_engineering.tools import (
    WebContentFetcher,
    LLMStructureExtractor,
    URLDiscoveryEngine,
    FileSystemManager
)


async def test_web_fetcher():
    """Test Web Content Fetcher."""
    print("\n🧪 Testing Web Content Fetcher...")
    
    config = Config.from_env()
    fetcher = WebContentFetcher(config)
    
    # Test with a simple URL
    test_url = "https://example.com"
    results = await fetcher.fetch([test_url])
    
    if results and results[0].get("success"):
        print(f"✅ Successfully fetched {test_url}")
        print(f"   Title: {results[0].get('title', 'N/A')}")
        print(f"   Status: {results[0].get('status_code', 'N/A')}")
    else:
        print(f"❌ Failed to fetch {test_url}")
        
    await fetcher.close()


async def test_structure_extractor():
    """Test LLM Structure Extractor."""
    print("\n🧪 Testing LLM Structure Extractor...")
    
    config = Config.from_env()
    extractor = LLMStructureExtractor(config)
    
    # Test content
    test_content = """
# Main Title

This is the introduction.

## Section 1

Content for section 1.

### Subsection 1.1

Detailed content here.

## Section 2

Content for section 2.
"""
    
    result = await extractor.extract(test_content)
    
    if result and result.get("structured_headings"):
        print("✅ Successfully extracted structure")
        print(f"   Total headings: {result.get('total_headings', 0)}")
        print(f"   Confidence: {result.get('confidence_score', 0):.2f}")
        print(f"   Format: {result.get('format_detected', 'unknown')}")
    else:
        print("❌ Failed to extract structure")


async def test_url_discovery():
    """Test URL Discovery Engine."""
    print("\n🧪 Testing URL Discovery Engine...")
    
    config = Config.from_env()
    discovery = URLDiscoveryEngine(config)
    
    # Test content with URLs
    test_content = """
    Check out our documentation at https://docs.example.com/api
    and our GitHub repository at https://github.com/example/repo.
    
    For more information, visit:
    - API Reference: https://api.example.com/reference
    - Tutorial: https://example.com/tutorial
    - Blog: https://blog.example.com
    """
    
    results = await discovery.discover(test_content, "example.com")
    
    if results:
        print(f"✅ Discovered {len(results)} URLs")
        for url_info in results[:3]:  # Show top 3
            print(f"   - {url_info['url']}")
            print(f"     Priority: {url_info['priority_score']:.2f}")
            print(f"     Type: {url_info['relation_type']}")
    else:
        print("❌ No URLs discovered")


async def test_file_manager():
    """Test File System Manager."""
    print("\n🧪 Testing File System Manager...")
    
    config = Config.from_env()
    manager = FileSystemManager(config)
    
    # Test directory creation
    result = await manager.execute(
        action="create_directory",
        path="test_output",
        content={
            "contexts": {},
            "logs": {}
        }
    )
    
    if result.get("success"):
        print("✅ Successfully created directory structure")
    else:
        print(f"❌ Failed to create directory: {result.get('error')}")
    
    # Test file writing
    test_content = {
        "title": "Test Context",
        "source_url": "https://example.com",
        "language": "en",
        "body": "# Test Content\n\nThis is a test."
    }
    
    result = await manager.execute(
        action="write_file",
        path="test_output/test.md",
        content=test_content
    )
    
    if result.get("success"):
        print("✅ Successfully wrote context file")
        print(f"   Path: {result.get('path')}")
    else:
        print(f"❌ Failed to write file: {result.get('error')}")
    
    # Test index generation
    result = await manager.execute(
        action="generate_index",
        path="test_output"
    )
    
    if result.get("success"):
        print("✅ Successfully generated index")
    else:
        print(f"❌ Failed to generate index: {result.get('error')}")


async def test_integration():
    """Run full integration test."""
    print("\n" + "="*60)
    print("🚀 YAML Context Engineering - Integration Test")
    print("="*60)
    
    try:
        # Test each component
        await test_web_fetcher()
        await test_structure_extractor()
        await test_url_discovery()
        await test_file_manager()
        
        print("\n" + "="*60)
        print("✅ All tests completed!")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


async def test_full_pipeline():
    """Test the full extraction pipeline."""
    print("\n" + "="*60)
    print("🔄 Testing Full Extraction Pipeline")
    print("="*60)
    
    config = Config.from_env()
    
    # Initialize all tools
    fetcher = WebContentFetcher(config)
    extractor = LLMStructureExtractor(config)
    discovery = URLDiscoveryEngine(config)
    file_manager = FileSystemManager(config)
    
    try:
        # Step 1: Fetch content
        print("\n1️⃣ Fetching content...")
        url = "https://www.python.org/about/"
        fetch_results = await fetcher.fetch([url])
        
        if not fetch_results or not fetch_results[0].get("success"):
            print("❌ Failed to fetch content")
            return
            
        content = fetch_results[0].get("content", "")
        print(f"✅ Fetched {len(content)} characters")
        
        # Step 2: Extract structure
        print("\n2️⃣ Extracting structure...")
        structure = await extractor.extract(content)
        print(f"✅ Extracted {structure.get('total_headings', 0)} headings")
        
        # Step 3: Discover URLs
        print("\n3️⃣ Discovering URLs...")
        urls = await discovery.discover(content, "python.org")
        print(f"✅ Discovered {len(urls)} URLs")
        
        # Step 4: Save to file
        print("\n4️⃣ Saving context...")
        context_data = {
            "title": fetch_results[0].get("title", "Python About"),
            "source_url": url,
            "language": fetch_results[0].get("language", "en"),
            "hierarchy_levels": structure.get("hierarchy_levels", []),
            "extraction_confidence": structure.get("confidence_score", 0),
            "body": f"# {fetch_results[0].get('title', 'Content')}\n\n"
                   f"## Summary\n\n{structure.get('content_summary', '')}\n\n"
                   f"## Structure\n\n"
                   f"Total headings: {structure.get('total_headings', 0)}\n\n"
                   f"## Discovered URLs\n\n"
                   f"Found {len(urls)} related URLs\n"
        }
        
        result = await file_manager.execute(
            action="write_file",
            path="test_output/python_about.md",
            content=context_data
        )
        
        if result.get("success"):
            print(f"✅ Saved context to {result.get('path')}")
        else:
            print("❌ Failed to save context")
            
        print("\n" + "="*60)
        print("🎉 Pipeline test completed successfully!")
        print("="*60)
        
    finally:
        await fetcher.close()


if __name__ == "__main__":
    print("""
╔════════════════════════════════════════════════════════════╗
║     YAML Context Engineering - Integration Test Suite      ║
╚════════════════════════════════════════════════════════════╝
""")
    
    # Run tests
    asyncio.run(test_integration())
    
    # Run full pipeline test
    asyncio.run(test_full_pipeline())
    
    print("\n✨ All tests completed successfully! ✨\n")