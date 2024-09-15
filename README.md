Terminal News is a Python package for fetching and displaying news articles from Google News directly in the terminal. It allows users to fetch news based on specific topics, display articles in a nicely formatted table, and read the content of each article interactively.

Features:

Fetch and display news articles from Google News.
Paginate through articles, with the ability to read full content of selected articles.
View articles in a Rich-formatted table with alternate row styling for better readability.
Use DuckDuckGo to resolve links and extract article content.
Fully interactive experience with pagination and article viewing from the terminal.

Installation:

To install Terminal News, clone the repository and use the following command to install the package locally:

```bash

pip install .
```
Usage:

Once installed, you can run the application by typing the following command in your terminal:

```bash

news
```

You will be able to browse through articles, select them by entering their number, and paginate through pages.

Dependencies:

The following dependencies are required for Terminal News to work properly:

    **requests**: For making HTTP requests to Google News and other APIs.
    **beautifulsoup4**: For parsing HTML content and extracting news data.
    **newspaper3k**: For extracting and processing article text from news websites.
    **rich**: For displaying tables and formatted text in the terminal.
    **duckduckgo_search**: For resolving article links using DuckDuckGo.

All dependencies are automatically installed when you install the package.

Configuration:

The package uses a configuration file (settings.ini) for setting the language and the topic for the news articles.

An example `settings.ini`:

makefile
```bash
[DEFAULT]
lang = en
topic = CAAqJggKIiBDQkFTRWdvSUwyMHZNRFZxYUdjU0FtbDBHZ0pKVkNnQVAB
```
_    lang: Language of the articles (e.g., en for English, it for Italian).
    topic: Topic ID for Google News to filter specific types of news._

License:

This project is licensed under the MIT License.