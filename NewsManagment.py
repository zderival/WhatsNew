import uuid
from datetime import datetime, timedelta, timezone
import requests
from dateutil import parser
import os
import pandas as pd
api_key = os.getenv("NEWS_API_KEY")

api_url = f"https://newsapi.org/v2/everything?q=keyword&apiKey={api_key}"
api_url2 = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={api_key}"


headers = {
    "Authorization": f"Bearer {api_key}"
}

class Article:
    def __init__(self, id, title, source, publishedAt, url, topic, author):
        self.id = id
        self.title = title
        self.source = source
        self.publishedAt = publishedAt
        self.url = url
        self.topic = topic
        self.author = author
    def __str__(self):
        return f"{self.title} - {self.source} - {self.url}\n"
    def __repr__(self):
        return f"{self.title} - {self.source} - {self.url}\n"


# Fetches articles from API
def fetch_articles(url, params= None, page_size=20):
    if params is None:
        params = {}
    global total_number_of_articles_fetched
    articles = []
    params["pageSize"] = page_size
    response = requests.get(url, headers=headers, params = params)
    data = response.json()
    for article_data in data.get("articles", []):
        published_at_dt = parser.isoparse(article_data["publishedAt"]).replace(tzinfo=timezone.utc)
        article = Article(
            id = uuid.uuid4(),
            title=article_data.get("title", ""),
            source=article_data.get("source", {}).get("name", ""),
            publishedAt=published_at_dt,
            url=article_data.get("url", ""),
            topic=article_data.get("category", ""),
            author=article_data.get("author", "")
        )
        articles.append(article)
    total_number_of_articles_fetched = data.get("totalResults", 0)
    return articles

def articles_to_df(articles):
    data = {
        "title": [a.title for a in articles],
        "source": [a.source for a in articles],
        "article": articles
    }
    df = pd.DataFrame(data)
    df["combined"] = df["title"] + " " + df["source"]
    return df
#Dict for finding specific articles
ids = {}
def print_article(url, params = None, page_size = 20):
    #Holds all articles that were fetched
    articles = fetch_articles(url, params, page_size)
    for i, article in enumerate(articles,start=1):
        print(f"{i}) {article}")
        ids[i] = article
    print(f"{len(articles)} articles found")
    return articles, ids

def articles_isEmpty(user_list,user):
    if len(user_list) == 0:
        return True
    else: return False

def prompt_articles_save(articles, user):
    ask_to_save_articles = input("Are there articles you wish to save? (yes/no): ").strip().lower()
    save_article_choice = []

    if ask_to_save_articles == "yes":
        try:
            choices_input = input("Enter the numbers of the articles you wish to save (separated by spaces): ").strip()
            save_article_choice = [int(x) for x in choices_input.split()]

            if save_article_choice:
                user.profile.new_manager.save_articles(save_article_choice, user)
            else:
                print("No valid article numbers entered.")

        except ValueError:
            print("Invalid input. Please enter numbers only.")
    else:
        print("No articles saved.")
class NewsManager:
    def __init__(self):
        pass

    @staticmethod
    def filter_topics(user_list):
        user_topics = user_list
        preferred_articles = [] #Save for ML/AI recommendations later
        formatted = [topic.title() for topic in user_topics]
        output = ",".join(formatted)
        if len(user_topics) == 1:
            print(f"{output} is your preference")
        else:
            print(f"{output} are your preferences")
        return preferred_articles

    @staticmethod
    def filter_by_date(articles, time_range):
        now = datetime.now(timezone.utc)
        if time_range == "Last 24 hours":
            cutoff = now - timedelta(hours=24)
        elif time_range == "Past week":
            cutoff = now - timedelta(days=7)
        elif time_range == "Past month":
            cutoff = now - timedelta(days=30)
        elif time_range == "Past year":
            cutoff = now - timedelta(days=365)
        else:
            return articles
        return [a for a in articles if a.publishedAt >= cutoff]

    def sort_articles(self, user_list, sort_how, filter_date_bool, filter_date):
        if filter_date_bool:
            user_list = self.filter_by_date(user_list,filter_date)

        if sort_how == "A-Z":
            return sorted(user_list, key= lambda x: x.title)
        elif sort_how == "Z-A":
            return sorted(user_list, key= lambda x: x.title, reverse=True)

    @staticmethod
    def fetch_articles_by_preferences(user_list):
        pass

    @staticmethod
    def save_articles(choice_list,user):
        global num
        for num in choice_list:
            if num in ids:
                article = ids[num]
                user.profile.saved_articles.append(article)
            else:
                print(f"Article number {num} does not exist.")
        print(f"{len(choice_list)} articles saved to your profile!")

        #you're looking through the list to read the values of ids that the user wanted to save

        # Articles - articles that were fetched to get a list of articles
        # choice_list - list of ids/(articles) the user wants to save

    @staticmethod
    def remove_articles(choice_list, user):
            # convert input to integers
        nums = [int(x) for x in choice_list]

        # remove duplicates and sort highest → lowest
        nums = sorted(set(nums), reverse=True)

        for num in nums:
            if 1 <= num <= len(user.profile.saved_articles):
                user.profile.saved_articles.pop(num - 1)
            else:
                print(f"Article number {num} does not exist.")

    @staticmethod
    def search_articles(search, page_size = 20):
        search = search.strip()
        url = f"https://newsapi.org/v2/everything"
        params = {"q": search,
                  "apikey": api_key,
                  }
        return print_article(url,params, page_size)

