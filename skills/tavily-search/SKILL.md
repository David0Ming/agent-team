# Tavily Search

**Name**: tavily-search  
**Description**: AI-optimized search using Tavily API with fallback chain (Tavily > SerpAPI > Serper > DuckDuckGo)

## Usage

Search with automatic fallback:
```bash
python3 search.py "your query" [num_results]
```

Search with Tavily only:
```bash
python3 tavily.py "your query" [search_depth] [max_results]
```

## Configuration

Set environment variables:
```bash
export TAVILY_API_KEY="your_tavily_key"
export SERPAPI_KEY="your_serpapi_key"
export SERPER_API_KEY="your_serper_key"
```

## Features

- **Tavily**: AI-optimized search with content extraction
- **SerpAPI**: Google search results
- **Serper**: Fast Google search API
- **DuckDuckGo**: Free fallback option

## Files

- `search.py`: Main search with fallback chain
- `tavily.py`: Tavily-only search with advanced options
