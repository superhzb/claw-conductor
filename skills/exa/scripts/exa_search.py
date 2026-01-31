#!/usr/bin/env python3
"""
Exa Web Search - Semantic search that understands intent.

Usage:
    python3 exa_search.py "your query" [options]

Example:
    python3 exa_search.py "machine learning applications in healthcare" --numResults 5
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("EXA_API_KEY")
API_URL = "https://api.exa.ai/search"

def search(query, numResults=5, useAutoprompt=True, type="neural", **filters):
    """Perform a semantic web search using Exa API."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "query": query,
        "numResults": numResults,
        "useAutoprompt": useAutoprompt,
        "type": type
    }

    # Add filters if provided
    if "domains" in filters and filters["domains"]:
        payload["domain"] = {"exclude": False, "values": filters["domains"].split(",")}
    if "excludeDomains" in filters and filters["excludeDomains"]:
        payload["domain"] = {"exclude": True, "values": filters["excludeDomains"].split(",")}
    if "startPublishedDate" in filters and filters["startPublishedDate"]:
        payload["startPublishedDate"] = filters["startPublishedDate"]
    if "endPublishedDate" in filters and filters["endPublishedDate"]:
        payload["endPublishedDate"] = filters["endPublishedDate"]
    if "category" in filters and filters["category"]:
        payload["category"] = filters["category"]

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

def format_results(results):
    """Format search results for display."""

    if not results.get("results"):
        return "No results found."

    output = []
    for i, result in enumerate(results["results"], 1):
        output.append(f"\n{i}. {result.get('title', 'No title')}")
        output.append(f"   URL: {result.get('url', 'N/A')}")
        output.append(f"   Score: {result.get('score', 'N/A')}")
        if result.get('publishedDate'):
            output.append(f"   Published: {result['publishedDate']}")
        if result.get('author'):
            output.append(f"   Author: {result['author']}")
        output.append(f"   Snippet: {result.get('text', 'No snippet')[:200]}...")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Exa semantic web search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--numResults", type=int, default=5, help="Number of results (1-10)")
    parser.add_argument("--noAutoprompt", action="store_true", help="Disable autoprompt")
    parser.add_argument("--type", default="neural", choices=["neural", "keyword", "auto", "hybrid", "fast", "magic", "deep"], help="Search type")
    parser.add_argument("--domains", help="Comma-separated list of allowed domains")
    parser.add_argument("--excludeDomains", help="Comma-separated list of domains to exclude")
    parser.add_argument("--startPublishedDate", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--endPublishedDate", help="End date (YYYY-MM-DD)")
    parser.add_argument("--category", help="Category filter")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: EXA_API_KEY environment variable not set.")
        print("Get an API key from https://exa.ai")
        sys.exit(1)

    filters = {
        "domains": args.domains,
        "excludeDomains": args.excludeDomains,
        "startPublishedDate": args.startPublishedDate,
        "endPublishedDate": args.endPublishedDate,
        "category": args.category
    }

    results = search(
        args.query,
        numResults=args.numResults,
        useAutoprompt=not args.noAutoprompt,
        type=args.type,
        **filters
    )

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))

if __name__ == "__main__":
    main()
