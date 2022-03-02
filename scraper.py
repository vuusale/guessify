import requests
from bs4 import BeautifulSoup as bs
import re
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
}

def scraper(url):
    html = requests.get(url, headers=headers, verify=False).text
    soup = bs(html, "html.parser")
    url_pieces = url.split("/")[:3]
    base_url = url_pieces[0] + "//" + url_pieces[2]
    images = image_scraper(soup, base_url)
    texts = text_scraper(soup)
    return {"texts": texts, "images": images}
    
        
def image_scraper(soup, base_url):
    images = []
    image_tags = soup.find_all("img")
    for img in image_tags:
        src = img.get("src")
        # Handle relative path
        if "http://" not in src and "https://" not in src and src[:2] !=  "//": 
            src = base_url + src
        images.append(src)
    return images


def text_scraper(soup):
    all_paragraphs = soup.find_all("p")
    all_texts = [] 
    buffer = ""
    for tag in all_paragraphs:
        # Skip tags with nested paragraphs
        if tag.find_all("p"):
            continue
        buffer += tag.text
        if len(buffer) <= 100:
            # Next paragraph will be added to buffer
            buffer += "\n"
            continue
        all_texts.append(buffer)
        buffer = ""
    return all_texts


if __name__ == "__main__":
    result = scraper("https://www.worldanimalprotection.org/blogs/intensive-livestock-farming-harming-people-animals-and-planet")
    print(f"This page has {len(result['texts'])} paragraphs and {len(result['images'])} images")