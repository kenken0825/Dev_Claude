"""Main entry point for YAML Context Engineering MCP Server."""

import asyncio
import sys
import logging
import click
from pathlib import Path
from typing import Optional

from .server import YamlContextServer
from .config import Config
from .utils.logging import setup_logging


@click.command()
@click.option(
    "--host",
    default="localhost",
    help="Host to bind the server to",
)
@click.option(
    "--port",
    default=3000,
    type=int,
    help="Port to bind the server to",
)
@click.option(
    "--log-level",
    default="INFO",
    type=click.Choice(["DEBUG", "INFO", "WARNING", "ERROR"]),
    help="Logging level",
)
@click.option(
    "--output-dir",
    type=click.Path(path_type=Path),
    default="generated_contexts",
    help="Base directory for generated context files",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True, path_type=Path),
    help="Path to configuration file",
)
def main(
    host: str,
    port: int,
    log_level: str,
    output_dir: Path,
    config_file: Optional[Path],
) -> None:
    """Start the YAML Context Engineering MCP Server."""
    # Setup logging
    setup_logging(log_level)
    logger = logging.getLogger(__name__)
    
    # Load configuration
    config = Config.from_env()
    config.log_level = log_level
    config.output.output_base_directory = output_dir
    
    # Override with config file if provided
    if config_file:
        logger.info(f"Loading configuration from {config_file}")
        # TODO: Implement config file loading
    
    # Validate configuration
    try:
        config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Create and start server
    server = YamlContextServer(config)
    
    logger.info(f"Starting YAML Context Engineering MCP Server on {host}:{port}")
    logger.info(f"Output directory: {config.output.output_base_directory}")
    
    try:
        asyncio.run(server.run(host, port))
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error(f"Server error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()