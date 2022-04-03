from email.mime import image
import uuid
from bs4 import BeautifulSoup
import requests
import shutil
from urllib.parse import urljoin

def download_images(images):
    image_locations = []
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, "html.parser")
    # images = soup.findAll("img")
    for image in images:
        # if url[0:2] != "//" and "svg" not in image.attrs["src"]:
        filename = str(uuid.uuid4())
        r = requests.get(image, stream=True)
        if r.status_code == 200:
            image_location = "images/normal/" + filename + ".jpg"
            image_locations.append(image_location)
            with open(image_location, "wb") as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)
    return image_locations