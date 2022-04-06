from flask import Flask, render_template, request
import scraper, requests
import convert
from imageCollector import download_images
from imageclassifier import classify_images
from text_classifier.classifier import classify_texts

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		url = request.form.get('url')
		# threshold = request.form.get('threshold')
		# width = request.form.get('width')
		# height = request.form.get('height')
		scraper_result = scraper.scraper(url, int(threshold)) # Calling scraper function
		images = download_images(url)
		#texts = scraper_result["texts"]
		#classified_texts = classify_texts(texts)
		#convert.convert2grayscale(images, int(width), int(height))
		classified_images = classify_images(images)
		return render_template('index.html', classified_images=classified_images, classified_texts=classify_texts)
	return render_template('index.html')

@app.route('/upload', methods=['GET','POST'])
def upload_route():
	if request.method == 'POST':
	    uploaded_file = request.files['file']
	    if uploaded_file.filename != '':
	    	url = 'http://127.0.0.1:8000'
	    	uploaded_file.save(uploaded_file.filename)
	    	files = {'image':open(uploaded_file.filename, 'rb')}
	    	res = requests.post(url, files=files)
	    	predicted_label = res.text.split('Predicted label: <b>')[1].split('</b>')[0]
	    	return render_template('upload.html',result=predicted_label)

	return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
