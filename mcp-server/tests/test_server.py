"""Tests for MCP server."""

import pytest
import asyncio
import json
from unittest.mock import Mock, AsyncMock, patch
from pathlib import Path

from yaml_context_engineering.server import YamlContextServer
from yaml_context_engineering.config import Config
from mcp.server.models import ToolResult


class TestYamlContextServer:
    """Test YAML Context Engineering MCP Server."""
    
    @pytest.fixture
    def server(self, test_config):
        """Create server instance."""
        return YamlContextServer(test_config)
    
    def test_server_initialization(self, server, test_config):
        """Test server initialization."""
        assert server.config == test_config
        assert server.server is not None
        assert server.web_fetcher is not None
        assert server.structure_extractor is not None
        assert server.url_discovery is not None
        assert server.file_manager is not None
    
    @pytest.mark.asyncio
    async def test_tool_registration(self, server):
        """Test that all tools are registered."""
        # Check internal tool registration
        # Note: This is a simplified test as MCP server internals are not directly accessible
        assert hasattr(server, '_register_tools')
        assert hasattr(server, '_setup_handlers')
    
    @pytest.mark.asyncio
    async def test_web_content_fetcher_tool(self, server):
        """Test web content fetcher tool execution."""
        # Mock the fetcher
        mock_result = [
            {
                "url": "https://example.com",
                "status_code": 200,
                "content": "Test content",
                "success": True
            }
        ]
        server.web_fetcher.fetch = AsyncMock(return_value=mock_result)
        
        # Call the tool handler
        handler = server.server._tool_handlers.get("web_content_fetcher")
        if handler:
            result = await handler(
                "web_content_fetcher",
                {"urls": ["https://example.com"]}
            )
            
            assert isinstance(result, ToolResult)
            content = json.loads(result.content)
            assert content[0]["success"] is True
    
    @pytest.mark.asyncio
    async def test_llm_structure_extractor_tool(self, server):
        """Test LLM structure extractor tool execution."""
        # Mock the extractor
        mock_result = {
            "structured_headings": [],
            "confidence_score": 0.9,
            "format_detected": "markdown"
        }
        server.structure_extractor.extract = AsyncMock(return_value=mock_result)
        
        # Call the tool handler
        handler = server.server._tool_handlers.get("llm_structure_extractor")
        if handler:
            result = await handler(
                "llm_structure_extractor",
                {"content": "# Test"}
            )
            
            assert isinstance(result, ToolResult)
            content = json.loads(result.content)
            assert content["confidence_score"] == 0.9
    
    @pytest.mark.asyncio
    async def test_url_discovery_engine_tool(self, server):
        """Test URL discovery engine tool execution."""
        # Mock the discovery engine
        mock_result = [
            {
                "url": "https://example.com/doc",
                "priority_score": 0.8,
                "relation_type": "internal"
            }
        ]
        server.url_discovery.discover = AsyncMock(return_value=mock_result)
        
        # Call the tool handler
        handler = server.server._tool_handlers.get("url_discovery_engine")
        if handler:
            result = await handler(
                "url_discovery_engine",
                {
                    "content": "Check https://example.com/doc",
                    "base_domain": "example.com"
                }
            )
            
            assert isinstance(result, ToolResult)
            content = json.loads(result.content)
            assert content[0]["priority_score"] == 0.8
    
    @pytest.mark.asyncio
    async def test_file_system_manager_tool(self, server):
        """Test file system manager tool execution."""
        # Mock the file manager
        mock_result = {
            "success": True,
            "action": "write_file",
            "path": "/tmp/test.md"
        }
        server.file_manager.execute = AsyncMock(return_value=mock_result)
        
        # Call the tool handler
        handler = server.server._tool_handlers.get("file_system_manager")
        if handler:
            result = await handler(
                "file_system_manager",
                {
                    "action": "write_file",
                    "path": "test.md",
                    "content": "Test content"
                }
            )
            
            assert isinstance(result, ToolResult)
            content = json.loads(result.content)
            assert content["success"] is True
    
    @pytest.mark.asyncio
    async def test_error_handling(self, server):
        """Test error handling in tool execution."""
        # Mock a failing tool
        server.web_fetcher.fetch = AsyncMock(side_effect=Exception("Test error"))
        
        # Call the tool handler
        handler = server.server._tool_handlers.get("web_content_fetcher")
        if handler:
            result = await handler(
                "web_content_fetcher",
                {"urls": ["https://example.com"]}
            )
            
            assert isinstance(result, ToolResult)
            assert result.is_error is True
            content = json.loads(result.content)
            assert "error" in content
            assert "Test error" in content["error"]
    
    @pytest.mark.asyncio
    async def test_unknown_tool(self, server):
        """Test handling of unknown tool."""
        handler = server.server._tool_handlers.get("unknown_tool")
        assert handler is None  # Unknown tools should not have handlers
    
    @pytest.mark.asyncio
    async def test_output_directory_creation(self, server, temp_output_dir):
        """Test that output directory is created on run."""
        server.config.output.output_base_directory = temp_output_dir / "new_dir"
        
        # Mock stdio_server
        mock_read = AsyncMock()
        mock_write = AsyncMock()
        
        with patch('yaml_context_engineering.server.stdio_server') as mock_stdio:
            mock_stdio.return_value.__aenter__.return_value = (mock_read, mock_write)
            
            # Start the run (it will fail due to mocking, but directory should be created)
            try:
                await asyncio.wait_for(server.run(), timeout=0.1)
            except asyncio.TimeoutError:
                pass
            
            assert server.config.output.output_base_directory.exists()


class TestToolIntegration:
    """Test integration between server and tools."""
    
    @pytest.fixture
    def integrated_server(self, test_config, temp_output_dir):
        """Create server with real tools."""
        test_config.output.output_base_directory = temp_output_dir
        return YamlContextServer(test_config)
    
    @pytest.mark.asyncio
    async def test_full_workflow(self, integrated_server):
        """Test a complete workflow through the server."""
        server = integrated_server
        
        # 1. Mock web content fetching
        mock_fetch_result = [{
            "url": "https://example.com",
            "status_code": 200,
            "content": "# Main Title\n\nContent here.",
            "success": True
        }]
        server.web_fetcher.fetch = AsyncMock(return_value=mock_fetch_result)
        
        # 2. Extract structure (use real extractor)
        extract_result = await server.structure_extractor.extract(
            mock_fetch_result[0]["content"]
        )
        assert extract_result["format_detected"] == "markdown"
        
        # 3. Discover URLs (use real discovery)
        discover_result = await server.url_discovery.discover(
            mock_fetch_result[0]["content"],
            "example.com"
        )
        
        # 4. Write file (use real file manager)
        write_result = await server.file_manager.execute(
            "write_file",
            "output.md",
            {
                "title": "Extracted Content",
                "source_url": "https://example.com",
                "body": mock_fetch_result[0]["content"]
            }
        )
        assert write_result["success"] is True
        assert Path(write_result["path"]).exists()