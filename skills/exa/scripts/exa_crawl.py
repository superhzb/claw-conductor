#!/usr/bin/env python3
"""
Exa Content Crawler - Extract full content from URLs.

Usage:
    python3 exa_crawl.py "https://example.com/article" [options]

Example:
    python3 exa_crawl.py "https://example.com/article" --text
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("EXA_API_KEY")
API_URL = "https://api.exa.ai/contents"

def crawl(urls, text=True, **options):
    """Extract content from URLs using Exa API."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "urls": urls if isinstance(urls, list) else [urls],
        "text": text
    }

    # Add optional parameters
    if "subpages" in options and options["subpages"]:
        payload["subpages"] = options["subpages"]
    if "subpageTarget" in options and options["subpageTarget"]:
        payload["subpageTarget"] = options["subpageTarget"]

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

def format_results(results):
    """Format crawled content for display."""

    if not results.get("results"):
        return "No content found."

    output = []
    for i, result in enumerate(results["results"], 1):
        output.append(f"\n{i}. {result.get('url', 'N/A')}")
        output.append(f"   Title: {result.get('title', 'N/A')}")

        if result.get('author'):
            output.append(f"   Author: {result.get('author')}")
        if result.get('publishedDate'):
            output.append(f"   Published: {result.get('publishedDate')}")

        if result.get('text'):
            text = result['text']
            output.append(f"\n   Content Preview ({len(text)} chars):")
            output.append(f"   {text[:500]}{'...' if len(text) > 500 else ''}")

        if result.get('subpages'):
            output.append(f"\n   Subpages ({len(result['subpages'])}):")
            for j, subpage in enumerate(result['subpages'][:3], 1):
                output.append(f"      {j}. {subpage.get('title', 'N/A')}: {subpage.get('url', 'N/A')}")
            if len(result['subpages']) > 3:
                output.append(f"      ... and {len(result['subpages']) - 3} more")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Exa content crawler")
    parser.add_argument("urls", nargs="+", help="URL(s) to crawl")
    parser.add_argument("--noText", action="store_true", help="Don't extract text content")
    parser.add_argument("--subpages", action="store_true", help="Also crawl linked pages")
    parser.add_argument("--subpageTarget", help="Subpage target (homepage, etc.)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: EXA_API_KEY environment variable not set.")
        print("Get an API key from https://exa.ai")
        sys.exit(1)

    options = {
        "subpages": args.subpages,
        "subpageTarget": args.subpageTarget
    }

    results = crawl(args.urls, text=not args.noText, **options)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))

if __name__ == "__main__":
    main()
