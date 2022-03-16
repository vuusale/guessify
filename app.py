from flask import Flask, render_template, request
import scraper
import convert
from imageCollector import download_images

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		url = request.form.get('url')
		threshold = request.form.get('threshold')
		width = request.form.get('width')
		height = request.form.get('height')
		scraper_result = scraper.scraper(url, int(threshold)) # Calling scraper function
		images = download_images(url)
		convert.convert2grayscale(images, int(width), int(height))
		return render_template('index.html', result=scraper_result)
	return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
