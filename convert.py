from PIL import Image
import os

FOLDER = "./images"

def convert2grayscale(filename):
    img = Image.open(os.path.join(FOLDER, filename))
    img = img.convert("L").resize((28, 28))
    img.save(os.path.join(FOLDER, filename))

if __name__ == "__main__":
    filename = "cat.jpg"
    convert2grayscale(filename)