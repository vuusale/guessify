# Guessify

This is a deep learning powered web scraper that extracts paragraphs and images from a web page and classifies them with the help of an artificial neural network.

## Setup
1. Create virtual env: `virtualenv venv`
2. Install requirements: `pip install -r requirements`
3. Install pytorch: `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113`
4. Download model, tokenizer and label encoder from [here](https://drive.google.com/drive/folders/1vbcoxmtzY6V-2lVl2PeSswlha44xKCO5?usp=sharing) and move to text_classifier folder
5. Navigate to image_classifier folder and run `python manage.py runserver`
6. Start flask server with `flask run`.
7. Give the below article as input:

https://ottawacitizen.com/news/world/how-nokia-enabled-russian-hacking-and-made-millions-doing-it-new-york-times/wcm/f066ee3c-f799-40d5-a10f-836e5ace62d1