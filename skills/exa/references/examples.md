# Exa Usage Examples

Real-world examples and patterns for using Exa's AI-powered search.

## Quick Examples

### Basic Web Search

```bash
python3 scripts/exa_search.py "machine learning applications in healthcare"
```

### Search with Filters

```bash
python3 scripts/exa_search.py "AI news" \
  --domains openai.com,anthropic.com \
  --startPublishedDate "2025-01-01" \
  --numResults 5
```

### Crawl a URL

```bash
python3 scripts/exa_crawl.py "https://example.com/article"
```

### Company Research

```bash
python3 scripts/exa_company.py "OpenAI" --numResults 3
```

### Deep Research

```bash
python3 scripts/exa_deep_research.py start "climate change solutions"
# Wait, then check status:
python3 scripts/exa_deep_research.py check <research_id>
```

### LinkedIn Profile Search

```bash
python3 scripts/exa_linkedin.py "machine learning engineer" --numResults 5
```

## Use Case Examples

### 1. Research a Topic

**Goal:** Learn about a complex topic with multiple perspectives

```bash
# Start deep research
python3 scripts/exa_deep_research.py start "pros and cons of nuclear energy" --numLearnings 20

# Check results (research_id from output)
python3 scripts/exa_deep_research.py check abcd1234
```

**Alternative:** Manual search + crawl

```bash
# Get relevant articles
python3 scripts/exa_search.py "nuclear energy pros cons" --numResults 10

# Crawl specific articles for full content
python3 scripts/exa_crawl.py "https://example.com/article1"
python3 scripts/exa_crawl.py "https://example.com/article2"
```

### 2. Competitive Intelligence

**Goal:** Research a competitor's products, news, and positioning

```bash
# Search for company news
python3 scripts/exa_search.py "Anthropic Claude updates" --numResults 10

# Get company info
python3 scripts/exa_company.py "Anthropic" --numResults 3

# Search LinkedIn posts from company
python3 scripts/exa_linkedin.py "Anthropic" --type post --numResults 10

# Find similar companies
curl -X POST https://api.exa.ai/findSimilar \
  -H "Content-Type: application/json" \
  -H "x-api-key: $EXA_API_KEY" \
  -d '{"url": "https://anthropic.com", "numResults": 10}'
```

### 3. Lead Generation

**Goal:** Find prospects matching criteria

```bash
# Find profiles at specific companies
python3 scripts/exa_linkedin.py "product manager at Google" --numResults 20

# Search for people with specific expertise
python3 scripts/exa_linkedin.py "AI researcher Stanford" --numResults 15

# Find companies in a space
python3 scripts/exa_company.py "AI healthcare startups" --numResults 10
```

### 4. Content Research

**Goal:** Gather sources for articles or reports

```bash
# Find recent articles on a topic
python3 scripts/exa_search.py "AI regulation 2024" \
  --startPublishedDate "2024-01-01" \
  --numResults 15

# Filter to authoritative sources
python3 scripts/exa_search.py "quantum computing breakthrough" \
  --domains nature.com,science.org,arxiv.org \
  --numResults 10

# Crawl multiple URLs for full content
python3 scripts/exa_crawl.py \
  "https://nature.com/article1" \
  "https://science.org/article2" \
  "https://arxiv.org/article3"
```

### 5. Industry Trend Analysis

**Goal:** Understand emerging trends in an industry

```bash
# Deep research on trends
python3 scripts/exa_deep_research.py start "AI trends 2025" --numLearnings 25

# Search recent news
python3 scripts/exa_search.py "AI industry trends" \
  --category news \
  --startPublishedDate "2025-01-01" \
  --numResults 15

# Find companies in the space
python3 scripts/exa_company.py "generative AI startups" --numResults 10
```

### 6. Academic Research

**Goal:** Find academic papers and research on a topic

```bash
# Search academic sources
python3 scripts/exa_search.py "transformer architecture papers" \
  --domains arxiv.org,scholar.google.com,nature.com \
  --numResults 10

# Deep research for comprehensive overview
python3 scripts/exa_deep_research.py start "large language model training techniques"
```

### 7. Job Market Research

**Goal:** Understand job market and opportunities

```bash
# Find job postings via LinkedIn
python3 scripts/exa_linkedin.py "machine learning engineer hiring" --type post --numResults 20

# Search for companies hiring
python3 scripts/exa_search.py "machine learning engineer jobs" --numResults 10

# Find companies in the space
python3 scripts/exa_company.py "AI companies hiring" --numResults 10
```

### 8. Fact Checking

**Goal:** Verify claims or find authoritative sources

```bash
# Search for verification
python3 scripts/exa_search.py "climate change statistics 2024" \
  --domains nasa.gov,noaa.gov,ipcc.ch \
  --numResults 10

# Crawl authoritative sources
python3 scripts/exa_crawl.py "https://nasa.gov/climate-change-data"
```

## Code Examples

### Python with Direct API Calls

```python
import requests
import os

API_KEY = os.environ["EXA_API_KEY"]
API_URL = "https://api.exa.ai/search"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

payload = {
    "query": "machine learning applications",
    "numResults": 5,
    "useAutoprompt": True
}

response = requests.post(API_URL, headers=headers, json=payload)
results = response.json()

for result in results["results"]:
    print(f"{result['title']}: {result['url']}")
```

### Batch Crawling

```python
import requests
import os

API_KEY = os.environ["EXA_API_KEY"]
API_URL = "https://api.exa.ai/contents"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

urls = [
    "https://example.com/article1",
    "https://example.com/article2",
    "https://example.com/article3"
]

payload = {
    "urls": urls,
    "text": True
}

response = requests.post(API_URL, headers=headers, json=payload)
results = response.json()

for result in results["results"]:
    print(f"{result['title']}: {len(result['text'])} characters")
```

### Deep Research with Status Polling

```python
import requests
import os
import time

API_KEY = os.environ["EXA_API_KEY"]
API_URL = "https://api.exa.ai/deepResearch"

headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

# Start research
payload = {
    "query": "quantum computing applications",
    "numResults": 10,
    "numLearnings": 15
}

response = requests.post(API_URL, headers=headers, json=payload)
research_id = response.json()["id"]

# Poll for completion
while True:
    response = requests.get(f"{API_URL}/{research_id}", headers=headers)
    result = response.json()

    if result["status"] == "completed":
        print("Research complete!")
        for learning in result["learnings"]:
            print(f"- {learning}")
        break
    elif result["status"] == "failed":
        print(f"Research failed: {result.get('error')}")
        break

    time.sleep(5)
```

## Common Patterns

### Pattern 1: Search Then Crawl

```bash
# Step 1: Find relevant URLs
python3 scripts/exa_search.py "topic" --numResults 5 > results.json

# Step 2: Extract URLs (jq or other tool)
cat results.json | jq -r '.results[].url' > urls.txt

# Step 3: Crawl all URLs
python3 scripts/exa_crawl.py $(cat urls.txt)
```

### Pattern 2: Filter by Authority

```bash
# Authoritative news sources
python3 scripts/exa_search.py "topic" \
  --domains nytimes.com,washingtonpost.com,reuters.com,apnews.com

# Academic sources
python3 scripts/exa_search.py "topic" \
  --domains nature.com,science.org,arxiv.org,scholar.google.com

# Government sources
python3 scripts/exa_search.py "topic" \
  --domains nasa.gov,noaa.gov,census.gov,gov.uk
```

### Pattern 3: Temporal Filtering

```bash
# Last 30 days
python3 scripts/exa_search.py "topic" \
  --startPublishedDate "$(date -v-30d +%Y-%m-%d)"

# This year
python3 scripts/exa_search.py "topic" \
  --startPublishedDate "$(date +%Y-01-01)"

# Specific date range
python3 scripts/exa_search.py "topic" \
  --startPublishedDate "2024-01-01" \
  --endPublishedDate "2024-12-31"
```

### Pattern 4: Combining Multiple Sources

```bash
# Get company info
python3 scripts/exa_company.py "OpenAI" > company.json

# Get recent news
python3 scripts/exa_search.py "OpenAI updates" --numResults 10 > news.json

# Get LinkedIn activity
python3 scripts/exa_linkedin.py "OpenAI" --type post --numResults 10 > linkedin.json

# Combine analysis
cat company.json news.json linkedin.json | jq
```

## Tips & Tricks

1. **Use autoprompt**: Let Exa optimize queries for better semantic understanding

2. **Combine tools**: Start with broad search, then crawl specific URLs for detail

3. **Leverage deep research**: Use for complex topics requiring multiple iterations

4. **Filter strategically**: Use domain filters for credibility, date filters for relevance

5. **Batch when possible**: Crawl multiple URLs in one request for efficiency

6. **Check research status**: Deep research takes time - poll the status endpoint

7. **Use categories**: Category filters help narrow down results by type

8. **Iterate**: Use one search's results to inform the next query
