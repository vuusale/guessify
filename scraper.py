import re
import requests
from bs4 import BeautifulSoup as bs
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
}

def scraper(url, threshold):
    html = requests.get(url, headers=headers, verify=False).text
    soup = bs(html, "html.parser")
    url_pieces = url.split("/")[:3]
    base_url = url_pieces[0] + "//" + url_pieces[2]
    images = image_scraper(soup, base_url)
    texts = text_scraper(soup, threshold)
    # return f"The webpage contains {len(texts)} paragraphs and {len(images)} images."
    return {"texts": texts, "images": images}
    
        
def image_scraper(soup, base_url):
    images = []
    image_tags = soup.find_all("img")
    for img in image_tags:
        if img.has_attr("src"):
            src = img.get("src")
            # Handle relative path
            if "http://" not in src and "https://" not in src and src[:2] != "//": 
                src = base_url + src
            images.append(src)
    return images


def text_scraper(soup, threshold, tag="p"):
    all_paragraphs = soup.find_all(tag)
    all_texts = []
    buffer = ""
    for tag in all_paragraphs:
        # Skip tags with nested paragraphs
        if tag.find_all(tag):
            continue
        buffer += tag.text
        if len(buffer) < threshold:
            # Next paragraph will be added to buffer
            buffer += "\n"
            continue
        words = re.findall("[a-zA-Z0-9']+", buffer)
        all_texts.append(words)
        buffer = ""
    return all_texts


if __name__ == "__main__":
    result = scraper("https://www.worldanimalprotection.org/blogs/intensive-livestock-farming-harming-people-animals-and-planet", 100)
    print(f"This page has {len(result['texts'])} paragraphs and {len(result['images'])} images")
    print(result['texts'])