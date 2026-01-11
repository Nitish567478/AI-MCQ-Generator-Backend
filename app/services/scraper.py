import requests
from bs4 import BeautifulSoup

def scrape_wikipedia(url: str):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title = soup.find("h1").get_text()
    content = soup.find("div", {"id": "mw-content-text"})

    paragraphs = [p.get_text() for p in content.find_all("p")]
    summary = paragraphs[0] if paragraphs else ""

    sections = [h.get_text() for h in content.find_all("h2")]

    text = "\n".join(paragraphs)

    return {
        "title": title,
        "summary": summary,
        "text": text,
        "sections": sections,
        "raw_html": response.text
    }
