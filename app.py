from flask import Flask, render_template, request
import scraper

app = Flask(__name__)

@app.route('/', methods=['GET','POST'])
def index():
	if request.method == 'POST':
		url = request.form.get('url')
		scraper_result = scraper.scraper(url) # Calling scraper function
		return render_template('index.html', result=scraper_result)
	return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
