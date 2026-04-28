import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from NewsManagment import fetch_articles, articles_to_df
import os

api_key = os.getenv("NEWS_API_KEY")
def fetch_potential_articles(preferences, page_size):
    potential_articles = []
    for preference in preferences:
        url = "https://newsapi.org/v2/everything"
        params = {"q": preference, "apiKey": api_key}
        fetched_articles = fetch_articles(url,params=params,page_size=page_size)
        potential_articles.extend(fetched_articles)
    return potential_articles

def get_recommendations(saved_articles,potential_articles):
    # Save user's saved articles lists, as well as their preferred topic list

    # 1. Convert preferred topic list to DataFrame (df)
    potential_articles_df = articles_to_df(potential_articles)

    # If no saved articles, just return potential_articles as is
    if not saved_articles:
        return potential_articles_df["article"].tolist()

    # If saved articles exist, rank by similarity
    saved_articles_df = articles_to_df(saved_articles)

    # 2. Combine the two df's and reset their indices to collaborate together
    all_texts = pd.concat([saved_articles_df["combined"], potential_articles_df["combined"]], ignore_index=True)

    # 3. Run TF-IDF
    # Term Frequency - Inverse Document Frequency is a method from scikit-learn used for retrieving information
    # to evaluate how important a word is to a document in relation to a larger collection of documents.

    # Term Frequency (TF): Measures how often a word appears in a document. A higher frequency suggests greater importance.
    # If a term appears frequently in a document, it is likely relevant to the document’s content.

    # Inverse Document Frequency (IDF): Reduces the weight of common words across multiple documents
    # while increasing the weight of rare words.
    # If a term appears in fewer documents, it is more likely to be meaningful and specific.

    vectorizer = TfidfVectorizer(stop_words="english")
    #  vectorizer - the process of converting non-numerical data (typically raw text)
    #  into numerical feature vectors that machine learning algorithms can process
    tfidf_matrix = vectorizer.fit_transform(all_texts)

    # fit(data) - calculates the parameters from the input data,
    # the vectorizer reads all the text and learns the vocabulary.
    # It figures out every unique word across all articles and decides how important each word is
    # based on how often it appears everywhere.

    # transform(data) - uses the parameters learned in the fit stage to actually modify the data.
    # now it takes each article and converts it into a row of numbers based on what it just learned.
    # Each number in that row corresponds to a word in the vocabulary and
    # represents how important that word is specifically to that article

    #fit_transform(data) - is doing both methods at the same time. And returns a rows of numbers from the collection of articles
    # essentially resembling a matrix

    # 4. Split back into saved and candidate vectors
    saved_vectors = tfidf_matrix[:len(saved_articles_df)]
    potential_vectors = tfidf_matrix[len(saved_articles_df):]
    # Slicing the matrix between the saved articles df and everything after that (potential articles df)
    # In my case, after TF-IDF runs, each article becomes a vector.
    # A vector is just a list of numbers that represents something.
    # Each number in that list corresponds to a word in the vocabulary.
    # The 0s mean that word doesn't appear in the article. The non-zero numbers represent how important that word is to that article.
    # So the vector is essentially the article's fingerprint in number form.
    # Saved_vectors - A set of vectors from users saved article list, one vector per saved article
    # potential_vectors - A set of vectors from user's preference list, one vector per saved article

    # 5. Build user profile and score candidates
    user_profile = saved_vectors.mean(axis=0)
    # Averages all the saved article vectors together into one vector.
    # This represents the user's overall taste in a mathematical summary of what they tend to read.
    # axis=0 means average column by column (word by word) across all rows (articles).

    scores = cosine_similarity(user_profile, potential_vectors)[0]
    # Compares the user's taste profile against every candidate article and produces a similarity score for each one between 0 and 1.
    # The closer to 1, the more similar to what the user likes. [0] just flattens the result into a simple list.

    # 6. Rank and return top results
    potential_articles_df["score"] = scores
    top = potential_articles_df.sort_values("score", ascending=False).head(10)
    return top["article"].tolist()
# Adds the scores as a new column to the candidate DataFrame,
# sorts highest to lowest, takes the top 10,
# then returns the actual Article objects from that article column as a plain Python list.
