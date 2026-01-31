#!/usr/bin/env python3
"""
Exa Deep Research - Multi-step AI-powered research on complex topics.

Usage:
    python3 exa_deep_research.py start "your research question"
    python3 exa_deep_research.py check <research_id>

Example:
    python3 exa_deep_research.py start "climate change solutions"
    python3 exa_deep_research.py check abcd1234
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("EXA_API_KEY")
API_URL = "https://api.exa.ai/deepResearch"

def start_research(query, numResults=5, numLearnings=10):
    """Start a deep research session."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "query": query,
        "numResults": numResults,
        "numLearnings": numLearnings
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

def check_research(research_id):
    """Check the status and results of a research session."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    response = requests.get(f"{API_URL}/{research_id}", headers=headers)
    response.raise_for_status()

    return response.json()

def format_start_results(results):
    """Format start research results."""

    research_id = results.get("id")
    status = results.get("status")

    output = []
    output.append(f"Research ID: {research_id}")
    output.append(f"Status: {status}")
    output.append(f"Query: {results.get('query', 'N/A')}")

    if status == "completed":
        output.append(f"\nResearch Complete!")
        output.append(f"\nLearnings ({len(results.get('learnings', []))}):")
        for i, learning in enumerate(results.get('learnings', []), 1):
            output.append(f"\n{i}. {learning}")

        if results.get('sources'):
            output.append(f"\nSources:")
            for j, source in enumerate(results['sources'][:5], 1):
                output.append(f"   {j}. {source.get('title', 'N/A')}: {source.get('url', 'N/A')}")
            if len(results['sources']) > 5:
                output.append(f"   ... and {len(results['sources']) - 5} more")

    elif status == "processing":
        output.append("\nResearch in progress...")
        output.append("Run this command again with the research ID to check status:")
        output.append(f"python3 exa_deep_research.py check {research_id}")

    elif status == "failed":
        output.append(f"\nResearch failed: {results.get('error', 'Unknown error')}")

    return "\n".join(output)

def format_check_results(results):
    """Format check research results."""

    status = results.get("status")

    output = []
    output.append(f"Research ID: {results.get('id', 'N/A')}")
    output.append(f"Status: {status}")

    if status == "completed":
        output.append(f"\nResearch Complete!")
        output.append(f"Query: {results.get('query', 'N/A')}")
        output.append(f"\nLearnings ({len(results.get('learnings', []))}):")
        for i, learning in enumerate(results.get('learnings', []), 1):
            output.append(f"\n{i}. {learning}")

        if results.get('sources'):
            output.append(f"\nSources:")
            for j, source in enumerate(results['sources'][:5], 1):
                output.append(f"   {j}. {source.get('title', 'N/A')}: {source.get('url', 'N/A')}")
            if len(results['sources']) > 5:
                output.append(f"   ... and {len(results['sources']) - 5} more")

    elif status == "processing":
        output.append("\nResearch still in progress...")
        output.append("Check again in a few moments.")

    elif status == "failed":
        output.append(f"\nResearch failed: {results.get('error', 'Unknown error')}")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Exa deep research")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    # Start command
    start_parser = subparsers.add_parser("start", help="Start a new research session")
    start_parser.add_argument("query", help="Research question")
    start_parser.add_argument("--numResults", type=int, default=5, help="Number of search results")
    start_parser.add_argument("--numLearnings", type=int, default=10, help="Number of learnings to extract")
    start_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    # Check command
    check_parser = subparsers.add_parser("check", help="Check research status")
    check_parser.add_argument("research_id", help="Research ID from start command")
    check_parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: EXA_API_KEY environment variable not set.")
        print("Get an API key from https://exa.ai")
        sys.exit(1)

    if args.command == "start":
        results = start_research(args.query, numResults=args.numResults, numLearnings=args.numLearnings)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(format_start_results(results))

    elif args.command == "check":
        results = check_research(args.research_id)
        if args.json:
            print(json.dumps(results, indent=2))
        else:
            print(format_check_results(results))

    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
