from PIL import Image
import os

NORMALFOLDER = "images/normal"
GRAYFOLDER = "images/gray"

def convert2grayscale(filenames, width, height):
	for filename in filenames:
	    img = Image.open(os.path.join(filename))
	    img = img.convert("L").resize((width, height))
	    img.save(os.path.join(GRAYFOLDER, os.path.basename(filename)))