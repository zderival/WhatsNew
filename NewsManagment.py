import uuid
from datetime import datetime, timedelta, timezone

import psycopg2
import requests
from dateutil import parser
import os
import pandas as pd
from psycopg2.extras import RealDictCursor


import db

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
        return f"{self.title}\n{self.source}\n{self.url}\n"
    def __repr__(self):
        return f"{self.title}\n{self.source}\n{self.url}\n"


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

def articles_isEmpty(user_list):
    if len(user_list) == 0:
        return True
    else: return False

class NewsManager:
    def __init__(self):
        pass

    @staticmethod
    # will return saved preference data from DB
    def filter_topics(user_list):
        user_topics = user_list
        formatted = [topic.title() for topic in user_topics]
        output = ",".join(formatted)
        return output

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
    def save_articles(choice_list,ids,user):
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory= RealDictCursor)
        for num in choice_list:
            if num in ids:
                article = ids[num]
                try:
                    sql = """
                    INSERT INTO saved_article (id,user_id,title,source,url)
                        VALUES (%s,%s,%s,%s,%s)
                          """
                    cursor.execute(sql,(uuid.uuid4(),user.id,article.title,article.source,article.url))
                except psycopg2.errors.UniqueViolation:
                    print("2 of the same article can not be saved.")
                    conn.rollback()
            else:
                print(f"Article number {num} does not exist.")
        conn.commit()
        print(f"{len(choice_list)} articles saved to your profile!")

        #you're looking through the list to read the values of ids that the user wanted to save

        # Articles - articles that were fetched to get a list of articles
        # choice_list - list of ids/(articles) the user wants to save

    @staticmethod
    def remove_articles(choice_list, ids):
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory= RealDictCursor)

            # convert input to integers
        nums = [int(x) for x in choice_list]

        # remove duplicates and sort highest → lowest
        nums = sorted(set(nums), reverse=True)

        for num in nums:
            if num in ids:
                sql = """
                DELETE FROM saved_article WHERE id = %s
                """
                cursor.execute(sql,(ids[num],))
            else:
                print(f"Article number {num} does not exist.")
        conn.commit()
    @staticmethod
    def search_articles(search, page_size = 20):
        search = search.strip()
        url = f"https://newsapi.org/v2/everything"
        params = {"q": search,
                  "apiKey": api_key,
                  }
        return fetch_articles(url,params, page_size)

    @staticmethod
    def get_saved_articles(user_id):
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory= RealDictCursor)
        sql = """
        SELECT id, title, source, url FROM saved_article WHERE user_id = %s
        """
        cursor.execute(sql,(user_id,))
        fetch = cursor.fetchall()
        return fetch

    @staticmethod
    def update_preferences(preference_list,user_id):
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory= RealDictCursor)
        sql = """ DELETE FROM user_prefrences WHERE user_id = %s
            """
        cursor.execute(sql, (user_id,))
        for preference in preference_list:
            sql2 = """
            INSERT INTO user_prefrences (id,user_id,topic)
                VALUES (%s,%s, %s)
            """
            cursor.execute(sql2,(uuid.uuid4(),user_id,preference))
        conn.commit()

    @staticmethod
    def get_preferences(user_id):
        conn = db.get_connection()
        cursor = conn.cursor(cursor_factory= RealDictCursor)
        sql = """
        SELECT topic FROM user_prefrences WHERE user_id = %s
        """
        cursor.execute(sql,(user_id,))
        fetch = cursor.fetchall()
        return fetch