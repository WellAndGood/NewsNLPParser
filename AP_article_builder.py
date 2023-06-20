from bs4 import BeautifulSoup
import requests
import json
from typing import Dict, Optional

# Works for Associated Press Articles
def ap_article_dict_builder(url: str) -> Dict:

    # Takes URL, outputs Beautiful Soup html
    response = requests.get(url)
    ap_article = BeautifulSoup(response.content, "html.parser")

    article_information = {}

    # Retrieves canonical link
    canonical_links = ap_article.find_all("link", rel="canonical")
    
    try:
        self_URL = canonical_links[-1].get("href")
    except IndexError:
        self_URL = "none"

    article_information["self_URL"] = self_URL

    # Retrieves article headline
    main_headline = ap_article.find_all("h1")
    main_headline = main_headline[0].text
    article_information["headline"] = main_headline

    # Retrieves article datetime metadata
    published_time = ap_article.find("meta", {"property": "article:published_time"}).get(
        "content"
    )
    modified_time = ap_article.find("meta", {"property": "article:modified_time"}).get(
        "content"
    )
    article_information["published_time"] = published_time
    article_information["modified_time"] = modified_time

    # Retrieves authors
    author_list = []
    scripts = ap_article.find(
        "script", attrs={"data-rh": "true", "type": "application/ld+json"}
    )
    json_script = json.loads(scripts.text)
    author_list = json_script["author"]
    article_information["author(s)"] = author_list

    # Retrieves image data
    image_data = []
    try:
        image_url = json_script["image"]
    except KeyError:
        image_url = ""
    image_caption_div = ap_article.find_all("div", attrs={"data-key": "embed-caption"})
    image_caption = image_caption_div[0].text
    try:
        image_attribution = image_caption[-50:].replace(")", "").split("(")[1]
    except IndexError:
        image_attribution = ""

    image_data.append([image_url, image_caption, image_attribution])

    # Retrieves paragraph data
    paragraphCount = 0
    article_paragraphs = []

    article_content = ap_article.find_all(
        "div", {"class": "Article", "data-key": "article"}
    )
    inner_para = article_content[0].find_all("p")

    # Loops through the paragraphs to find inner information
    for index, para in enumerate(inner_para):

        paragraphCount += 1
        inner_text = para.text
        inner_links = para.find_all("a")
        content, href = "", ""

        # reset the array
        inner_link = []

        # Traverse the list to retrieve links and its associated text
        for link in inner_links:
            content = link.string.strip()
            href = link["href"]
            if href[0] == "/":
                href = "https://apnews.com" + href
            inner_link.append([content, href])
            para_ele = para.name
        article_paragraphs.append([index, inner_text, inner_link])

    article_information["mainContents"] = article_paragraphs

    return article_information

def ap_article_full_txt(url: str) -> Optional[str]:
    article_dict = ap_article_dict_builder(url)
    paragraph_contents = article_dict["mainContents"]

    entire_article = ""

    for i, content in enumerate(paragraph_contents):
        entire_article += f" {content[1]}"

    return entire_article