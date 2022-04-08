import os
import requests
from PIL import Image
import uuid
import requests
import shutil

NORMALFOLDER = "images/normal"
GRAYFOLDER = "images/gray"

def download_images(images):
	image_locations = []
    # page = requests.get(url)
    # soup = BeautifulSoup(page.content, 'html.parser')
    # images = soup.findAll('img')
	for image in images:
		if ('https://' in image or 'http://' in image) and '///' not in image and 'svg' not in image:
			filename = str(uuid.uuid4())
			r = requests.get(image, stream=True)
			if r.status_code == 200:
				image_location = "images/normal/" + filename + '.jpg'
				image_locations.append(image_location)
				with open(image_location, 'wb') as f:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)
	return image_locations

def convert2grayscale(filenames, width, height):
	for filename in filenames:
		img = Image.open(os.path.join(filename))
		img = img.convert("L").resize((width, height))
		img.save(os.path.join(GRAYFOLDER, os.path.basename(filename)))

def classify_images(images):
	predicted_labels = {}
	for image in images:
		files = {'image':open(image, 'rb')}
		res = requests.post('http://127.0.0.1:8000', files=files)
		try:
			predicted_label = res.text.split('Predicted label: <b>')[1].split('</b>')[0]
		except:
			predicted_label = "stage"
		predicted_labels[image] = predicted_label
	return predicted_labels

def remove_images(images):
	for image in images:
		try:
			os.remove(image)
		except:
			continue
	
def normalize_output(categories):
	result = {}
	for category in categories.values():
		if category not in result:
			result[category] = 1
		else:
			result[category] += 1
	return result

	