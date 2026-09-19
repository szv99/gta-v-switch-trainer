#!/usr/bin/env python3
"""
GTA V Nintendo Switch (Build 2699) - In-Memory GDB Trainer CLI
Main root entry point forwarding to framework/trainer.py
"""
import os
import sys
from pathlib import Path

# Add framework to module path
FRAMEWORK_DIR = Path(__file__).resolve().parent / 'framework'
if str(FRAMEWORK_DIR) not in sys.path:
    sys.path.insert(0, str(FRAMEWORK_DIR))

from trainer import main

if __name__ == '__main__':
    main()
