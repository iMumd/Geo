#!/usr/bin/env python3
# ═══════════════════════════════════════════════════════════════
# Geo Protection Bot - Main Entry Point
# ═══════════════════════════════════════════════════════════════

import asyncio
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nBot stopped by user")
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)