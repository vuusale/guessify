import html
import pickle
from typing import Text
import torch
import pandas as pd
from text_classifier.model import Text_Classifier, predict_single
import os

def classify_text(text: str) -> str:
    with open('./text_classifier/tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    with open('./text_classifier/labelencoder.pickle', 'rb') as handle:
        le = pickle.load(handle)

    with open('./text_classifier/embedding.pickle', 'rb') as handle:
        embedding_matrix = pickle.load(handle)

    model = Text_Classifier(embedding_matrix, le)
    model.load_state_dict(torch.load("./text_classifier/model.pt"))
    model.eval()
    model.cuda()
    return predict_single(text, model, tokenizer, le)

def classify_texts(texts: list) -> dict:
    results = {}
    for text in texts:
        text = ' '.join(text)
        outcome = classify_text(text)
        results[outcome] =  results[outcome] + 1 if outcome in results else 1
    return results

# news = """
# We are currently mid-phase between two eras: the pre- and post-digital age. It isn't unusual to think that you have understood “the power of the new” when you haven't.
# """
# print(classify_text(news))

'''
news = """North Korea has recently resumed digging tunnels and construction activities at its underground nuclear test site, according to five US officials. Commercially available satellite imagery had shown some indications of activity on the surface at Pyongyang's remote Punggye-ri nuclear test site.
It is not yet clear how soon the regime would be capable of testing a device at the site, as it depends on the pace of the activity, the officials say.
The preparations for a possible underground nuclear test come after North Korea tested its first suspected intercontinental ballistic missile since 2017 earlier this month.
"We remain concerned about the North Koreans -- their attempt to continue to improve their nuclear capability as well as their ballistic missile capability," Pentagon press secretary John Kirby told reporters Tuesday. Kirby declined to be more specific about what he was referring to on the regime's nuclear capability."""
outcome = predict_single(news, model, tokenizer, le)
print(outcome)

df = pd.read_csv('./test.csv')
total = len(df)
results = []
correct = 0
incorrect = 0
for index, row in df.iterrows():
    news = row['News']
    real_category = row['Category']
    outcome = predict_single(news, model, tokenizer, le)
    results.append({'review': html.unescape(news).replace('"',''), 'outcome': outcome}) 
    if real_category == outcome:
        correct += 1
    else:
        # print(f"Outcome: {outcome}, real category: {real_category}")
        incorrect += 1

print(f"[+] {correct / total * 100}% correct")
print(f"[-] {incorrect / total * 100}% incorrect")

[+] 87.57908055672712% correct                                        3        time=174.18s
[-] 12.420919443272881% incorrect
'''