"""
Web Research Tool for Development Team
"""

import requests
from bs4 import BeautifulSoup
from typing import Optional
from crewai.tools import BaseTool


class WebResearchTool(BaseTool):
    name: str = "Web Research Tool"
    description: str = "Tool for web research, documentation lookup, and technology information gathering"

    def _run(self, operation: str, query: str, url: Optional[str] = None) -> str:
        """
        Perform web research operations
        
        Args:
            operation: Research type (search, scrape, documentation)
            query: Search query or content to look for
            url: Specific URL to scrape (optional)
        """
        try:
            if operation == "search":
                return self._search_web(query)
            
            elif operation == "scrape" and url:
                return self._scrape_url(url)
            
            elif operation == "documentation":
                return self._search_documentation(query)
            
            else:
                return f"Unknown operation: {operation}"
                
        except Exception as e:
            return f"Error in web research: {str(e)}"
    
    def _search_web(self, query: str) -> str:
        """Search web for information"""
        try:
            # Using DuckDuckGo Instant Answer API (no API key required)
            url = f"https://api.duckduckgo.com/?q={query}&format=json&no_html=1&skip_disambig=1"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                result = f"Search results for: {query}\n\n"
                
                if data.get('Abstract'):
                    result += f"Summary: {data['Abstract']}\n\n"
                
                if data.get('RelatedTopics'):
                    result += "Related Topics:\n"
                    for topic in data['RelatedTopics'][:5]:
                        if isinstance(topic, dict) and 'Text' in topic:
                            result += f"- {topic['Text']}\n"
                
                return result if len(result) > 50 else "No detailed results found for this query"
            
            else:
                return f"Search failed with status code: {response.status_code}"
                
        except Exception as e:
            return f"Error searching web: {str(e)}"
    
    def _scrape_url(self, url: str) -> str:
        """Scrape content from a specific URL"""
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()
                
                # Get text content
                text = soup.get_text()
                
                # Clean up text
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = '\n'.join(chunk for chunk in chunks if chunk)
                
                # Limit text length
                if len(text) > 2000:
                    text = text[:2000] + "... (truncated)"
                
                return f"Content from {url}:\n\n{text}"
            
            else:
                return f"Failed to scrape URL. Status code: {response.status_code}"
                
        except Exception as e:
            return f"Error scraping URL: {str(e)}"
    
    def _search_documentation(self, query: str) -> str:
        """Search for documentation and technical resources"""
        try:
            # Search for documentation on common sites
            doc_sites = [
                f"site:docs.python.org {query}",
                f"site:developer.mozilla.org {query}",
                f"site:stackoverflow.com {query}",
                f"site:github.com {query}"
            ]
            
            results = []
            for site_query in doc_sites[:2]:  # Limit to 2 sites to avoid rate limiting
                try:
                    search_result = self._search_web(site_query)
                    if search_result and "No detailed results" not in search_result:
                        results.append(search_result)
                except:
                    continue
            
            if results:
                return "\n\n".join(results)
            else:
                return f"No documentation found for: {query}"
                
        except Exception as e:
            return f"Error searching documentation: {str(e)}"
