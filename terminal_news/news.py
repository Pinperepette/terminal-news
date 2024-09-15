from .news_google.news_google import fetch_articles 
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
import os

# Initialize the Rich console
console = Console()

# Fetch articles and link resolver from the news_google module
articles, link_resolver = fetch_articles()
ARTICLES_PER_PAGE = 20

# Function to display the table with articles and alternate background styles
def show_table(page=1):
    os.system('clear')  # Clear the terminal
    table = Table(title=f"Article List (Page {page})", border_style="green")
    table.add_column("#", justify="center", style="red")
    table.add_column("Date", justify="left", style="yellow")
    table.add_column(
        "Press the article number to read it, [green]'n'[/green] for next page, "
        "[yellow]'p'[/yellow] for previous page, [red]'q'[/red] to quit.", justify="left"
    )

    start = (page - 1) * ARTICLES_PER_PAGE
    end = start + ARTICLES_PER_PAGE
    page_articles = articles[start:end]

    # Add articles to the table with alternate row styles
    for i, article in enumerate(page_articles, start=start):
        row_style = "none" if i % 2 == 0 else "dim"  # Use "dim" for slightly lighter rows
        table.add_row(str(i), article['date'], article['title'], style=row_style)

    console.print(table)

# Function to display the selected article
def show_article(article):
    os.system('clear')  # Clear the terminal
    article_text = link_resolver.resolve_link(article['title'])
    article_content = article_text if article_text else "Content not available"

    # Format and display the article with a white border
    article_panel = Panel(
        f"[bold]{article['title']}[/bold]\n\n{article_content}",
        title=f"Article: {article['title']}",
        border_style="white"
    )
    
    console.print(article_panel)
    console.rule()

# Main loop for pagination and article selection
def main():
    current_page = 1
    total_pages = (len(articles) + ARTICLES_PER_PAGE - 1) // ARTICLES_PER_PAGE

    while True:
        show_table(current_page)
        user_input = console.input("Select an article: ")

        if user_input == 'q':
            os.system('clear')  # Clear the terminal when exiting
            break
        elif user_input == 'n' and current_page < total_pages:
            current_page += 1
        elif user_input == 'p' and current_page > 1:
            current_page -= 1
        else:
            try:
                article_index = int(user_input)
                if 0 <= article_index < len(articles):
                    show_article(articles[article_index])
                    console.input("Press 'p' to return to the list: ")
            except ValueError:
                console.print("Invalid input, please try again.")

if __name__ == "__main__":
    main()
