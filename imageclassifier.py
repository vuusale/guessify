import requests

def classify_images(images):
	print(images)
	predicted_labels = {}
	for image in images:
		files = {'image':open(image, 'rb')}
		res = requests.post('http://127.0.0.1:8000', files=files)
		predicted_label = res.text.split('Predicted label: <b>')[1].split('</b>')[0]
		predicted_labels[image] = predicted_label
	return predicted_labels