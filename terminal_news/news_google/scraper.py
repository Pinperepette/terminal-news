import urllib.request
from bs4 import BeautifulSoup as Soup
import re
from bs4 import ResultSet
import requests
from duckduckgo_search import DDGS
import trafilatura  # Sostituisce eventuali altre librerie di parsing

def build_response(url, headers):
    """
    Makes an HTTP request to the specified URL and returns the parsed result from the HTML page.
    """
    try:
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        page = response.read()
        content = Soup(page, "html.parser")  # Parse the HTML content
        
        result = content.find_all("article")  # Find all articles in the page
        return result
    except Exception as e:
        print(f"Error retrieving the page: {e}")
        return []

def remove_after_last_fullstop(s):
    """
    Removes everything after the last period in a string.
    """
    last_period_index = s.rfind('.')
    return s[:last_period_index + 1] if last_period_index != -1 else s

class GoogleNewsLinkResolver:
    """
    Class that resolves the original article link by searching on DuckDuckGo using the article title.
    """

    def resolve_link(self, article_title):
        """
        Search for multiple articles using the title on DuckDuckGo and return the text of the first valid article.
        """
        try:
            ddg_search = DDGS()
            # Perform a search on DuckDuckGo using the article title
            results = ddg_search.text(article_title, region='wt-wt', safesearch='Off', max_results=5)
            
            if results:
                # Create a list of links from the search results
                links = [result['href'] for result in results]
                # Test each link and attempt to extract the article text
                for link in links:
                    article_text = self.extract_article_text(link)
                    if article_text:  # If text extraction succeeds, return the text
                        return article_text
                return None  # Return None if no valid article is found
            else:
                return None  # Return None if no search results are found
        except Exception as e:
            print(f"Error during DuckDuckGo search: {e}")
            return None

    def extract_article_text(self, link):
        """
        Extracts the text of an article given a link using Trafilatura.
        """
        try:
            # Use Trafilatura to extract the article content
            downloaded = trafilatura.fetch_url(link)
            article_text = trafilatura.extract(downloaded)
            return article_text if article_text else None
        except Exception as e:
            print(f"Error extracting article text: {e}")
            return None
