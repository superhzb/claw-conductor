---
name: exa
description: "AI-powered web search and research using Exa API. Use when you need: (1) High-quality web search with semantic understanding, (2) Advanced search with specific filters (domain, date, topic), (3) Website crawling and content extraction, (4) Company research and LinkedIn search, (5) Deep research on complex topics. Alternative to Brave Search for better semantic results."
---

# Exa - AI-Powered Search & Research

## Quick Start

Get an API key from https://exa.ai, set it as `EXA_API_KEY`, then use scripts in `scripts/` or make direct HTTP requests.

## Core Capabilities

### 1. Web Search (`exa_search.py`)
Semantic search that understands intent, not just keywords.

```bash
python3 scripts/exa_search.py "machine learning applications in healthcare" --numResults 5
```

**Parameters:**
- `--numResults`: Number of results (1-10, default: 5)
- `--useAutoprompt`: Let Exa optimize query (default: true)
- `--type`: "neural" (default), "keyword", "auto", "hybrid", "fast", "magic", "deep"

### 2. Advanced Search (`exa_search.py` with filters)
Apply filters for precise results.

```bash
python3 scripts/exa_search.py "AI news" \
  --domains openai.com,anthropic.com \
  --startPublishedDate "2025-01-01"
```

**Filters:**
- `--domains`: Comma-separated list of allowed domains
- `--excludeDomains`: Domains to exclude
- `--startPublishedDate`, `--endPublishedDate`: Date range
- `--category`: Category filter (coding, ai, news, research, etc.)

### 3. Crawling (`exa_crawl.py`)
Extract full content from specific URLs.

```bash
python3 scripts/exa_crawl.py "https://example.com/article"
```

**Parameters:**
- `--text`: Extract main text content (default: true)
- `--subpages`: Also crawl linked pages
- `--subpageTarget`: Subpages to crawl (homepage, etc.)

### 4. Company Research (`exa_company.py`)
Comprehensive company analysis.

```bash
python3 scripts/exa_company.py "OpenAI" --numResults 3
```

Returns: Company description, website, employee count, LinkedIn profiles, funding info.

### 5. Deep Research (`exa_deep_research.py`)
Multi-step research on complex topics.

```bash
python3 scripts/exa_deep_research.py start "climate change solutions"
python3 scripts/exa_deep_research.py check <research_id>
```

Performs iterative research, refining the query based on findings.

### 6. LinkedIn Search (`exa_linkedin.py`)
Search LinkedIn profiles and posts.

```bash
python3 scripts/exa_linkedin.py "machine learning engineer" --numResults 5
```

**Parameters:**
- `--type`: "profile" or "post" (default: "profile")
- `--numResults`: Number of results

## API Details

For advanced usage, see [API Reference](references/api.md).

**Base URL:** `https://api.exa.ai`

**Endpoints:**
- `POST /search` - Web search
- `POST /contents` - Crawl URLs
- `POST /findSimilar` - Find similar content
- `POST /companySearch` - Company research
- `POST /linkedinSearch` - LinkedIn search

**Authentication:** Bearer token in `Authorization` header.

## Best Practices

1. **Use semantic queries**: Exa understands intent better than keyword search
   - Good: "how does quantum computing impact cryptography"
   - Bad: "quantum computing cryptography"

2. **Leverage filters**: Use `--domains` and date ranges for precision
   - Search only authoritative sources for sensitive topics
   - Limit to recent articles for breaking news

3. **Start with web search, then crawl**: Get URLs via search, extract content via crawl

4. **Use deep research for complex topics**: Let the AI iterate and refine research

5. **Combine with other tools**: Use Exa for discovery, then fetch specific pages via `web_fetch`

## When to Use Exa vs. Other Tools

| Task | Best Tool | Why |
|------|-----------|-----|
| General web search | Exa | Better semantic understanding |
| Real-time breaking news | Brave Search | Faster, fresher index |
| Simple keyword search | Either | Similar results |
| Company research | Exa | Structured company data |
| LinkedIn profiles | Exa | Dedicated endpoint |
| Content extraction | web_fetch | Direct, no API key needed |
| Complex research | Exa Deep Research | Multi-step AI refinement |

## Troubleshooting

**Error: Invalid API key**
- Verify key at https://exa.ai/dashboard
- Ensure `EXA_API_KEY` environment variable is set

**Empty results**
- Try enabling `--useAutoprompt` (default)
- Broaden query or remove filters
- Check if topic is too niche

**Rate limiting**
- Free tier: 1,000 requests/month
- Consider batching requests where possible
- See https://exa.ai/pricing for upgrade options

## Resources

- **scripts/**: Executable scripts for common operations
- **references/api.md**: Full API documentation
- **references/examples.md**: Code examples and patterns
