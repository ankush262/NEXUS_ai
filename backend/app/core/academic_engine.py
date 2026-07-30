import os
import requests
import urllib.parse
import xml.etree.ElementTree as ET
from scholarly import scholarly
from github import Github
from tavily import TavilyClient

# 1. GitHub Repository Fetcher (for Competitor Repos & License Analysis)
def fetch_github_repos(query: str, max_results: int = 2):
    results = []
    github_token = os.getenv("GITHUB_TOKEN")
    try:
        gh = Github(github_token) if github_token else Github()
        repos = gh.search_repositories(query=query, sort="stars")
        for repo in list(repos)[:max_results]:
            license_name = repo.license.name if repo.license else "No License Specified"
            results.append({
                "source": "GitHub",
                "title": repo.full_name,
                "description": repo.description or "No description",
                "license": license_name,
                "stars": repo.stargazers_count,
                "url": repo.html_url
            })
    except Exception as e:
        print(f"[Engine] GitHub notice: {e}")
    return results

# 2. Tavily Web Search (for Competitors & Market Research)
def fetch_tavily_web_search(query: str, max_results: int = 2):
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key:
        return []
    try:
        tavily = TavilyClient(api_key=tavily_key)
        response = tavily.search(query=f"competitors and startup market for {query}", max_results=max_results)
        return [{
            "source": "Tavily Web Search",
            "title": res.get("title"),
            "snippet": res.get("content"),
            "url": res.get("url")
        } for res in response.get("results", [])]
    except Exception as e:
        print(f"[Engine] Tavily notice: {e}")
    return []

# 3. Google Scholar Fetcher
def fetch_google_scholar(query: str, max_results: int = 2):
    results = []
    try:
        search_query = scholarly.search_pubs(query)
        for _ in range(max_results):
            pub = next(search_query)
            results.append({
                "source": "Google Scholar",
                "title": pub['bib'].get('title', 'No Title'),
                "authors": pub['bib'].get('author', 'Unknown'),
                "snippet": pub['bib'].get('abstract', 'No abstract available.'),
                "url": pub.get('pub_url', '')
            })
    except Exception as e:
        print(f"[Engine] Google Scholar notice: {e}")
    return results

# 4. IEEE Xplore Fetcher
def fetch_ieee_papers(query: str, max_results: int = 2):
    api_key = os.getenv("IEEE_API_KEY")
    if not api_key:
        return []
    url = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    params = {"apikey": api_key, "querytext": query, "max_records": max_results}
    results = []
    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            for article in res.json().get("articles", []):
                authors = [a.get("full_name", "") for a in article.get("authors", {}).get("authors", [])]
                results.append({
                    "source": "IEEE Xplore",
                    "title": article.get("title"),
                    "authors": ", ".join(authors),
                    "snippet": article.get("abstract", "No abstract available"),
                    "url": article.get("html_url") or article.get("pdf_url")
                })
    except Exception as e:
        print(f"[Engine] IEEE notice: {e}")
    return results

# 5. Wiley & Crossref Fetcher
def fetch_wiley_crossref_papers(query: str, max_results: int = 2):
    url = "https://api.crossref.org/works"
    params = {"query": query, "rows": max_results, "select": "title,author,URL,publisher,DOI"}
    results = []
    try:
        res = requests.get(url, params=params, timeout=5)
        if res.status_code == 200:
            items = res.json().get("message", {}).get("items", [])
            for item in items:
                authors_list = [f"{a.get('given', '')} {a.get('family', '')}" for a in item.get("author", [])]
                results.append({
                    "source": f"Wiley/Crossref ({item.get('publisher', 'Academic')})",
                    "title": item.get("title", ["No Title"])[0],
                    "authors": ", ".join(authors_list),
                    "url": item.get("URL", f"https://doi.org/{item.get('DOI', '')}")
                })
    except Exception as e:
        print(f"[Engine] Crossref notice: {e}")
    return results

# 6. Google News RSS Fetcher
def fetch_google_news(query: str, max_results: int = 2):
    encoded = urllib.parse.quote(query)
    rss_url = f"https://news.google.com/rss/search?q={encoded}&hl=en-US&gl=US&ceid=US:en"
    try:
        res = requests.get(rss_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=5)
        if res.status_code == 200:
            root = ET.fromstring(res.content)
            return [{
                "source": "Google News",
                "title": item.find('title').text,
                "url": item.find('link').text
            } for item in root.findall('./channel/item')[:max_results]]
    except Exception as e:
        print(f"[Engine] Google News notice: {e}")
    return []

# 🌐 Complete Consolidated Harvester
def gather_all_academic_and_web_data(query: str) -> list:
    print(f"\n🔍 [NEXUS Engine] Harvesting research sources for: '{query}'...")
    sources = []
    
    # Academic
    scholar = fetch_google_scholar(query)
    sources.extend(scholar)
    ieee = fetch_ieee_papers(query)
    sources.extend(ieee)
    wiley = fetch_wiley_crossref_papers(query)
    sources.extend(wiley)
    
    # Code & Competitors
    github_repos = fetch_github_repos(query)
    sources.extend(github_repos)
    tavily_web = fetch_tavily_web_search(query)
    sources.extend(tavily_web)
    
    # News
    news = fetch_google_news(query)
    sources.extend(news)
    
    print(f"✅ Total {len(sources)} live sources harvested across Scholar, IEEE, Wiley, GitHub, Tavily, and News.\n")
    return sources