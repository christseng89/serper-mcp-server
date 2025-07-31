#!/usr/bin/env python3
"""
Entry point for running the serper-mcp-server as a module.
"""

import asyncio
from serper_mcp_server.server import main

if __name__ == "__main__":
    asyncio.run(main()) 