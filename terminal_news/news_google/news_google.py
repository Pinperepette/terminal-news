import urllib.request
from .utils import lexical_date_parser, define_date
from .scraper import build_response, remove_after_last_fullstop
from newspaper import Article
from .scraper import GoogleNewsLinkResolver
import configparser
import os

def load_settings():
    """
    Load the settings.ini file and return 'lang' and 'topic' values.
    """
    config = configparser.ConfigParser()
    # Get the absolute path to the settings.ini file
    settings_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'settings.ini')
    # Read the settings.ini file
    config.read(settings_path)
    # Get 'lang' and 'topic' from the settings.ini file
    lang = config['DEFAULT']['lang']
    topic = config['DEFAULT']['topic']

    return lang, topic
def fetch_articles():
    """
    Fetch articles based on the loaded settings and return them along with the link resolver.
    """
    lang, topic = load_settings()

    # Initialize the NewsGoogle class and set the topic for the search
    news = NewsGoogle(lang=lang)
    news.set_topic(topic)
    news.search()

    return news.results(), news.link_resolver

class NewsGoogle:
    """
    Main class to perform news searches on Google News, with support for specific topics.
    """

    def __init__(self, lang="en", period="", start="", end="", encode="utf-8", region=None):
        """
        Initialize the NewsGoogle class with language, period, and other parameters.
        """
        self.__texts = []
        self.__links = []
        self.__results = []
        self.__totalcount = 0
        self.user_agent = 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:64.0) Gecko/20100101 Firefox/64.0'
        self.__lang = lang
        self.__period = period
        self.__start = start
        self.__end = end
        self.__encode = encode
        self.__exception = False
        self.__topic = None
        self.link_resolver = GoogleNewsLinkResolver()
        
        # Set the headers for the request, including region if specified
        if region:
            self.accept_language = f'{lang}-{region},{lang};q=0.9'
            self.headers = {'User-Agent': self.user_agent, 'Accept-Language': self.accept_language}
        else:
            self.headers = {'User-Agent': self.user_agent}

    def set_topic(self, topic_id):
        """
        Set a specific topic ID for the Google News search.
        """
        self.__topic = topic_id

    def search(self, key=None):
        """
        Perform a Google News search. If a topic is set, it searches for that topic.
        Otherwise, it performs a keyword-based search.
        """
        if self.__topic:
            self.url = f"https://news.google.com/topics/{self.__topic}?hl={self.__lang}&gl={self.__lang}&ceid={self.__lang}:it"
        else:
            self.__key = urllib.request.quote(key.encode(self.__encode))
            self.url = f"https://www.google.com/search?q={self.__key}&hl={self.__lang}&tbm=nws"
        
        self.get_page()

    def get_page(self, page=1):
        """
        Fetch the results page from Google News and parse the top news section.
        """
        # URL for the top news section
        self.url = f"https://news.google.com/topics/{self.__topic}?hl={self.__lang}&gl={self.__lang}&ceid={self.__lang}:it"

        # Get the HTML response and parse it using build_response
        result = build_response(self.url, self.headers)

        # Process each news item from the result
        for item in result:
            try:
                tmp_text = item.find("a", attrs={'jsaction': 'click:kkIcoc;'}).text.replace("\n", "") if item.find("a", attrs={'jsaction': 'click:kkIcoc;'}) else "No title available"
                tmp_link = item.find("a", attrs={'jsaction': 'click:kkIcoc;'}).get("href", "") if item.find("a", attrs={'jsaction': 'click:kkIcoc;'}) else "No link available"
                tmp_link = f'https://news.google.com{tmp_link}' if tmp_link.startswith('./') else tmp_link
                date_span = item.find('time')
                tmp_date = date_span.text if date_span else "No date available"
                tmp_datetime = define_date(tmp_date)
                tmp_desc = item.find('p').text if item.find('p') else "No description available"
                tmp_img = item.find("img").get("src", "") if item.find("img") else "No image available"

                self.__results.append({
                    'title': tmp_text,
                    'date': tmp_date,
                    'datetime': tmp_datetime,
                    'desc': tmp_desc,
                    'link': tmp_link,
                    'img': tmp_img
                })
            except Exception as e:
                print(f"Error during parsing: {e}")

    def results(self, sort=False):
        """
        Return the results of the search. If sort is True, the results are sorted by date.
        """
        return sorted(self.__results, key=lambda x: x['datetime'], reverse=True) if sort else self.__results

    def extract_article_text(self, url):
        """
        Extract the main text of an article given its final URL using the newspaper3k library.
        """
        try:
            final_url = self.link_resolver.resolve_link(url)
            if final_url:
                article = Article(final_url)
                article.download()
                article.parse()
                return article.text
            else:
                return "Unable to retrieve final article link"
        except Exception as e:
            print(f"Error extracting article text from {url}: {e}")
            return None
