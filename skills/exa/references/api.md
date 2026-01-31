# Exa API Reference

Complete API documentation for Exa's AI-powered search platform.

## Base URL

```
https://api.exa.ai
```

## Authentication

Include your API key in the `x-api-key` header:

```bash
curl -X POST https://api.exa.ai/search \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_API_KEY" \
  -d '{"query": "machine learning"}'
```

Or set as environment variable:

```bash
export EXA_API_KEY="your_api_key_here"
```

## Endpoints

### 1. Search (`/search`)

Semantic web search that understands intent.

**Method:** `POST`

**Request Body:**

```json
{
  "query": "string (required)",
  "numResults": 10,
  "useAutoprompt": true,
  "type": "web",
  "domain": {
    "exclude": false,
    "values": ["example.com", "test.org"]
  },
  "startPublishedDate": "2024-01-01",
  "endPublishedDate": "2024-12-31",
  "category": "research"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query (semantic understanding enabled) |
| `numResults` | int | No | 10 | Number of results (1-100) |
| `useAutoprompt` | bool | No | true | Let AI optimize the query |
| `type` | string | No | "neural" | "neural" (default), "keyword", "auto", "hybrid", "fast", "magic", "deep" |
| `domain` | object | No | - | Domain filters |
| `startPublishedDate` | string | No | - | ISO 8601 date format |
| `endPublishedDate` | string | No | - | ISO 8601 date format |
| `category` | string | No | - | Category filter (research, news, ai, etc.) |

**Response:**

```json
{
  "results": [
    {
      "title": "Article Title",
      "url": "https://example.com/article",
      "score": 0.95,
      "publishedDate": "2024-01-15",
      "author": "John Doe",
      "text": "Article snippet..."
    }
  ]
}
```

### 2. Contents (`/contents`)

Extract full content from URLs.

**Method:** `POST`

**Request Body:**

```json
{
  "urls": ["https://example.com/article1", "https://example.com/article2"],
  "text": true,
  "subpages": false,
  "subpageTarget": "homepage"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `urls` | array | Yes | - | List of URLs to crawl |
| `text` | bool | No | true | Extract text content |
| `subpages` | bool | No | false | Also crawl linked pages |
| `subpageTarget` | string | No | - | Subpage target (homepage, etc.) |

**Response:**

```json
{
  "results": [
    {
      "title": "Page Title",
      "url": "https://example.com/article",
      "author": "Author Name",
      "publishedDate": "2024-01-15",
      "text": "Full page content..."
    }
  ]
}
```

### 3. Find Similar (`/findSimilar`)

Find similar content based on a URL or text.

**Method:** `POST`

**Request Body:**

```json
{
  "url": "https://example.com/reference-article",
  "numResults": 10
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `url` | string | Yes* | - | URL to find similar content for (or use `text`) |
| `text` | string | Yes* | - | Text to find similar content for (or use `url`) |
| `numResults` | int | No | 10 | Number of results |

### 4. Company Search (`/companySearch`)

Search for companies and get structured data.

**Method:** `POST`

**Request Body:**

```json
{
  "query": "OpenAI",
  "numResults": 5
}
```

**Response:**

```json
{
  "results": [
    {
      "name": "OpenAI",
      "website": "https://openai.com",
      "description": "AI research company",
      "logo": "https://logo-url...",
      "linkedin": "openai",
      "linkedinUrl": "https://linkedin.com/company/openai",
      "funding": {
        "amount": "$10B",
        "round": "Series D",
        "date": "2023-01-01"
      },
      "employees": 500,
      "twitter": "openai",
      "blog": "https://openai.com/blog",
      "tags": ["AI", "Machine Learning", "Technology"]
    }
  ]
}
```

### 5. LinkedIn Search (`/linkedinSearch`)

Search LinkedIn profiles and posts.

**Method:** `POST`

**Request Body:**

```json
{
  "query": "machine learning engineer",
  "numResults": 10,
  "type": "profile"
}
```

**Parameters:**

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search query |
| `numResults` | int | No | 10 | Number of results |
| `type` | string | No | "profile" | "profile" or "post" |

### 6. Deep Research (`/deepResearch`)

Multi-step AI-powered research on complex topics.

**Start Research:**

**Method:** `POST`

**Request Body:**

```json
{
  "query": "What are the best strategies for reducing carbon emissions?",
  "numResults": 10,
  "numLearnings": 15
}
```

**Response:**

```json
{
  "id": "abcd1234",
  "status": "processing",
  "query": "What are the best strategies for reducing carbon emissions?"
}
```

**Check Status:**

**Method:** `GET`

**URL:** `/deepResearch/{research_id}`

**Response (Completed):**

```json
{
  "id": "abcd1234",
  "status": "completed",
  "query": "What are the best strategies for reducing carbon emissions?",
  "learnings": [
    "Key insight 1...",
    "Key insight 2...",
    "Key insight 3..."
  ],
  "sources": [
    {
      "title": "Article Title",
      "url": "https://example.com/article"
    }
  ]
}
```

## Error Responses

All errors return a JSON object:

```json
{
  "error": "Error message",
  "statusCode": 400
}
```

**Common Error Codes:**

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Invalid API key |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error |

## Rate Limits

- **Free Tier:** 1,000 requests/month
- **Pro Tier:** 10,000 requests/month
- **Enterprise:** Custom limits

See https://exa.ai/pricing for details.

## Best Practices

1. **Use semantic queries:** Exa understands intent, not just keywords
   - Good: "how does quantum computing impact cryptography"
   - Bad: "quantum computing cryptography"

2. **Enable autoprompt:** Let AI optimize queries for better results

3. **Use filters:** Combine domain filters and date ranges for precision

4. **Batch operations:** Use `/contents` endpoint to process multiple URLs

5. **Deep research:** Use for complex topics that require multiple iterations

## SDKs

Official SDKs available:
- Python: `pip install exa-py`
- JavaScript: `npm install exa-js`

See https://docs.exa.ai for SDK documentation.

## Support

- Documentation: https://docs.exa.ai
- Pricing: https://exa.ai/pricing
- Support: support@exa.ai
