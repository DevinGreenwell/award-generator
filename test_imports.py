#!/usr/bin/env python3
"""Test script to debug import issues."""

import sys
import os
from pathlib import Path

# Add src to path
src_path = Path(__file__).parent / 'src'
sys.path.insert(0, str(src_path))

print(f"Python version: {sys.version}")
print(f"Current directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"src directory exists: {src_path.exists()}")
print(f"src contents: {list(src_path.iterdir()) if src_path.exists() else 'N/A'}")
print("-" * 60)

# Test each import individually
imports_to_test = [
    "award_engine",
    "award_engine.base",
    "award_engine.exceptions",
    "openai_client",
    "config",
    "validation",
    "session_manager",
    "citation_formatter",
    "cg_docx_export",
]

for module in imports_to_test:
    try:
        __import__(module)
        print(f"✓ Successfully imported: {module}")
    except Exception as e:
        print(f"✗ Failed to import {module}: {type(e).__name__}: {e}")
        
print("-" * 60)

# Test specific imports
try:
    from award_engine import AwardEngine, AwardEngineError, InsufficientDataError
    print("✓ Successfully imported from award_engine")
except Exception as e:
    print(f"✗ Failed to import from award_engine: {type(e).__name__}: {e}")

try:
    from openai_client import OpenAIClient
    print("✓ Successfully imported OpenAIClient")
except Exception as e:
    print(f"✗ Failed to import OpenAIClient: {type(e).__name__}: {e}")

try:
    from citation_formatter import CitationFormatter
    print("✓ Successfully imported CitationFormatter")
except Exception as e:
    print(f"✗ Failed to import CitationFormatter: {type(e).__name__}: {e}")

try:
    from cg_docx_export import generate_cg_compliant_docx
    print("✓ Successfully imported generate_cg_compliant_docx")
except Exception as e:
    print(f"✗ Failed to import generate_cg_compliant_docx: {type(e).__name__}: {e}")