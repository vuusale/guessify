# Guessify

This is a deep learning powered web scraper that extracts paragraphs and images from a web page and classifies them with the help of an artificial neural network.

## Setup
Execute setup script suitable to your operating system and start flask server with `flask run`.

### Text classifier
To train the model on Windows with the Cuda driver installed, run `pip3 install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu113`

Download model, tokenizer and label encoder from [here](https://drive.google.com/drive/folders/1vbcoxmtzY6V-2lVl2PeSswlha44xKCO5?usp=sharing)
