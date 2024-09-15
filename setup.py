from setuptools import setup, find_packages

setup(
    name='terminal_news',
    version='1.0.0',
    author='Pinperepette',
    author_email='pinperepette@gmail.com',
    description='A Python package for fetching and displaying news articles from Google News in the terminal',
    packages=find_packages(include=["terminal_news", "terminal_news.*"]),
    install_requires=[
        'requests',
        'beautifulsoup4',
        'newspaper3k',
        'rich',
        'duckduckgo_search',
        'dateparser',  # Add dateparser
        'lxml[html_clean]'  # Add lxml with html_clean
    ],
    include_package_data=True,
    package_data={'': ['settings.ini']},
    entry_points={
        'console_scripts': [
            'news=terminal_news.news:main',  # Questo eseguirà 'news.py'
        ],
    },
)
