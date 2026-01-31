#!/usr/bin/env python3
"""
Exa Company Research - Comprehensive company analysis.

Usage:
    python3 exa_company.py "company name" [options]

Example:
    python3 exa_company.py "OpenAI" --numResults 3
"""

import os
import sys
import json
import argparse
import requests

API_KEY = os.environ.get("EXA_API_KEY")
API_URL = "https://api.exa.ai/companySearch"

def search_companies(query, numResults=3):
    """Search for companies using Exa API."""

    headers = {
        "Content-Type": "application/json",
        "x-api-key": API_KEY
    }

    payload = {
        "query": query,
        "numResults": numResults
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    response.raise_for_status()

    return response.json()

def format_results(results):
    """Format company search results for display."""

    if not results.get("results"):
        return "No companies found."

    output = []
    for i, company in enumerate(results["results"], 1):
        output.append(f"\n{i}. {company.get('name', 'N/A')}")
        output.append(f"   Website: {company.get('website', 'N/A')}")
        output.append(f"   Description: {company.get('description', 'N/A')}")

        if company.get('logo'):
            output.append(f"   Logo: {company['logo']}")

        if company.get('linkedin'):
            output.append(f"   LinkedIn: {company['linkedin']}")

        if company.get('linkedinUrl'):
            output.append(f"   LinkedIn URL: {company['linkedinUrl']}")

        if company.get('funding'):
            funding = company['funding']
            output.append(f"   Funding:")
            if funding.get('amount'):
                output.append(f"      Amount: {funding['amount']}")
            if funding.get('round'):
                output.append(f"      Round: {funding['round']}")
            if funding.get('date'):
                output.append(f"      Date: {funding['date']}")

        if company.get('employees'):
            output.append(f"   Employees: {company['employees']}")

        if company.get('twitter'):
            output.append(f"   Twitter: {company['twitter']}")

        if company.get('blog'):
            output.append(f"   Blog: {company['blog']}")

        if company.get('tags'):
            output.append(f"   Tags: {', '.join(company['tags'])}")

    return "\n".join(output)

def main():
    parser = argparse.ArgumentParser(description="Exa company research")
    parser.add_argument("query", help="Company name or description")
    parser.add_argument("--numResults", type=int, default=3, help="Number of results (1-10)")
    parser.add_argument("--json", action="store_true", help="Output raw JSON")

    args = parser.parse_args()

    if not API_KEY:
        print("Error: EXA_API_KEY environment variable not set.")
        print("Get an API key from https://exa.ai")
        sys.exit(1)

    results = search_companies(args.query, numResults=args.numResults)

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results))

if __name__ == "__main__":
    main()
