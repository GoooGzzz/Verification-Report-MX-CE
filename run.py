#!/usr/bin/env python3
"""
Entry point for the Samsung Field Intelligence Dashboard
"""
import sys
import os

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

# Import and run the main application
from app.main import *