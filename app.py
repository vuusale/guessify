from flask import Flask, render_template, request
import scraper, requests
import validators
import pickle
from image_utils import classify_images, normalize_output, remove_images, download_images, convert2grayscale
from text_classifier.classifier import classify_texts, classify_text
from flask import jsonify, make_response

app = Flask(__name__)


@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		url = request.form.get('url')
		# threshold = request.form.get('threshold')
		threshold = 50
		if not validators.url(url):
			return render_template('index.html', error='Please supply a valid url')
		try:
			f = open('database.pickle', 'rb')
			database = pickle.load(f)
			f.close()
			if url in database:
				classified_texts = database[url]['classified_texts']
				classified_images = database[url]['classified_images']
				number_of_paragraphs = sum(classified_texts.values())
				number_of_images = sum(classified_images.values())
				return render_template('index.html', classified_images=classified_images, classified_texts=classified_texts, number_of_paragraphs=number_of_paragraphs, number_of_images=number_of_images, url=url, charts=True)
		except IOError:
			print('The first scrapping...')
			
		scraper_result = scraper.scraper(url, int(threshold))
		images = download_images(scraper_result["images"])
		texts = scraper_result["texts"]
		classified_texts = classify_texts(texts)
		# width = 28
		# height = 28
		# convert.convert2grayscale(images, int(width), int(height))
		image_categories = classify_images(images)
		classified_images = normalize_output(image_categories)
		number_of_paragraphs = sum(classified_texts.values())
		number_of_images = sum(classified_images.values())
		remove_images(images)
		scrap_result = {'classified_texts': classified_texts, 'classified_images': classified_images}
		try:
			database[url] = scrap_result
		except:
			database = {url: scrap_result}
		with open('database.pickle', 'wb') as f:
			pickle.dump(database, f)

		return render_template('index.html', classified_images=classified_images, classified_texts=classified_texts, number_of_paragraphs=number_of_paragraphs, number_of_images=number_of_images, charts=True)
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

@app.route('/singletext', methods=['GET', 'POST'])
def single_text():
	if request.method == 'POST':
		text = request.form.get('text')
		category = classify_text(text)
		return render_template('text.html', result=category)
	
	return render_template('text.html')

@app.route('/chart', methods=['GET'])
def chart():
	image_labels = []
	image_data = []
	text_labels = []
	text_data = []
	url = request.args.get('url')
	f = open('database.pickle', 'rb')
	database = pickle.load(f)
	f.close()
	if url in database:
		classified_texts = database[url]['classified_texts']
		classified_images = database[url]['classified_images']
		for label, d in classified_images.items():
			image_labels.append(label)
			image_data.append(d)
		for label, d in classified_texts.items():
			text_labels.append(label)
			text_data.append(d)
	return make_response(jsonify(data={'image_labels': image_labels, 'image_data': image_data, 'text_labels': text_labels, 'text_data': text_data}), 200)

if __name__ == '__main__':
    app.run(debug=True)
