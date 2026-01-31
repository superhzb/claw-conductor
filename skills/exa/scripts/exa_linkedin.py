#!/usr/bin/env python3
"""
Exa LinkedIn Search - Search LinkedIn profiles and posts.

Usage:
    python3 exa_linkedin.py "search query" [options]

Example:
    python3 exa_linkedin.py "machine learning engineer" --numResults 5
    python3 exa_linkedin.py "AI news" --type post --numResults 10
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("EXA_API_KEY")
API_URL = "https://api.exa.ai/linkedinSearch"

def search_linkedin(query, numResults=5, search_type="profile"):
    """Search LinkedIn using Exa API."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "query": query,
        "numResults": numResults,
        "type": search_type
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

def format_profile_results(results):
    """Format profile search results for display."""

    if not results.get("results"):
        return "No profiles found."

    output = []
    for i, profile in enumerate(results["results"], 1):
        output.append(f"\n{i}. {profile.get('title', 'N/A')}")
        output.append(f"   URL: {profile.get('url', 'N/A')}")

        if profile.get('name'):
            output.append(f"   Name: {profile['name']}")

        if profile.get('author'):
            output.append(f"   Author: {profile.get('author')}")

        if profile.get('headline'):
            output.append(f"   Headline: {profile['headline']}")

        if profile.get('summary'):
            summary = profile['summary']
            output.append(f"   Summary: {summary[:200]}{'...' if len(summary) > 200 else ''}")

    return "\n".join(output)

def format_post_results(results):
    """Format post search results for display."""

    if not results.get("results"):
        return "No posts found."

    output = []
    for i, post in enumerate(results["results"], 1):
        output.append(f"\n{i}. {post.get('title', 'N/A')}")
        output.append(f"   URL: {post.get('url', 'N/A')}")

        if post.get('author'):
            output.append(f"   Author: {post['author']}")

        if post.get('publishedDate'):
            output.append(f"   Published: {post['publishedDate']}")

        if post.get('text'):
            text = post['text']
            output.append(f"   Content: {text[:200]}{'...' if len(text) > 200 else ''}")

        if post.get('likes'):
            output.append(f"   Likes: {post['likes']}")

        if post.get('comments'):
            output.append(f"   Comments: {post['comments']}")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Exa LinkedIn search")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--numResults", type=int, default=5, help="Number of results (1-10)")
    parser.add_argument("--type", default="profile", choices=["profile", "post"], help="Search type")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: EXA_API_KEY environment variable not set.")
        print("Get an API key from https://exa.ai")
        sys.exit(1)

    results = search_linkedin(args.query, numResults=args.numResults, search_type=args.type)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        if args.type == "profile":
            print(format_profile_results(results))
        else:
            print(format_post_results(results))

if __name__ == "__main__":
    main()
