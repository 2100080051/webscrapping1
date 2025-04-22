import os
import requests
from dotenv import load_dotenv
from duckduckgo_search import DDGS
from bs4 import BeautifulSoup

load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

import time
def search_articles(query):
    results = []
    with DDGS() as ddgs:
        for r in ddgs.text(query, region='wt-wt', safesearch='Moderate', max_results=5):
            results.append({"title": r['title'], "href": r['href']})
            time.sleep(1)
    return results


def concatenate_content(articles):
    combined = ""
    for article in articles:
        try:
            html = requests.get(article["href"], timeout=5).text
            soup = BeautifulSoup(html, "html.parser")
            paragraphs = soup.find_all("p")
            text = "\n".join([p.get_text() for p in paragraphs])
            combined += f"\n\nTitle: {article['title']}\nURL: {article['href']}\n\n{text}\n"
        except Exception as e:
            combined += f"\n\n[Error reading {article['href']}] - {e}\n"
    return combined[:8000]

def generate_answer(context, query):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": f"Question: {query}\n\nContext:\n{context}"}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    try:
        res_json = response.json()
        if "choices" in res_json:
            return res_json["choices"][0]["message"]["content"]
        else:
            return f"❌ Groq API error: {res_json.get('error', 'Unknown error')}"
    except Exception as e:
        return f"❌ Failed to parse Groq response: {str(e)}"
