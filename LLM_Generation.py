import os
from google import genai
def llm_generation(preferences, saved_article, recommendations):
    saved_article = [f"{article.source} - {article.title}" for article in saved_article]
    recommendations = [f"{article.title} - {article.source}" for article in recommendations]
    preferences_join = ",".join(preferences)
    saved_article_join = ",".join(saved_article)
    recommendations_join = ",".join(recommendations)
    prompt = f"""
    You are an AI recommendation explainer.

Your task is to explain why a set of news articles was recommended to a user using ONLY the information provided below.

Input:
- User Preferences: {preferences_join}
- Previously Saved Articles: {saved_article_join}
- Recommended Articles (title and source): {recommendations_join}

Instructions:
1. Explain why these articles were recommended by identifying similarities between the user's preferences, previously saved articles, and the recommended article titles.
2. Base your explanation ONLY on the information provided. Do not assume user interests or invent article content beyond what can reasonably be inferred from the titles.
3. Provide a single overall summary of the recommended articles. The summary should describe the main topics and trends represented across all of the recommendations, not summarize each article individually.
4. After the summary, provide exactly three bullet points highlighting the key themes shared among the recommendations.
5. Finish with a conclusion of no more than two sentences explaining how the recommendations align with the user's demonstrated interests.

Output Format:

## Why These Articles Were Recommended
<Explain the reasoning behind the recommendations.>

## Overall Summary
<Write a cohesive 2–3 sentence summary describing the common content and topics represented by the recommended articles. If the titles do not provide enough information, state that the summary is inferred from the available titles.>

## Key Themes
- Theme 1
- Theme 2
- Theme 3

## Conclusion
<Maximum 2 sentences>

Important:
- Use only the provided information.
- Do not fabricate article details or user interests.
- Clearly indicate when conclusions are inferred from the article titles.
- Keep the response concise, objective, and easy to understand.
"""
    client = genai.Client(api_key=os.getenv("Gemini_API_KEY"))

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents= prompt
    )
    return response.text