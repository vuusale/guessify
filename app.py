import sys
from turtle import width
from convert import convert2grayscale
from flask import Flask, render_template, request
import scraper
from imageCollector import download_images
from text_classifier.classifier import classify_texts

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
	if request.method == "POST":
		url = request.form.get("url")
		threshold = request.form.get("threshold")
		# width = request.form.get("width")
		# height = request.form.get("height")
		width = 28
		height = 28
		scraper_result = scraper.scraper(url, int(threshold)) # Calling scraper function
		images = download_images(scraper_result["images"])
		texts = scraper_result["texts"]
		classified_texts = classify_texts(texts)
		convert2grayscale(images, int(width), int(height))
		return render_template("index.html", result=classified_texts, images=len(images))
	return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
