from unicodedata import category
import pandas as pd
from collections import Counter

if __name__ == "__main__":
    dataset = pd.read_csv('./old-files/dailyo before optim.csv')
    dataset['News'] = dataset['News_title'] + "." + dataset['News_headline']
    dataset.drop('Unnamed: 0', axis=1, inplace=True)
    dataset.drop('Unnamed: 0.1', axis=1, inplace=True)
    dataset.drop('News_title', axis=1, inplace=True)
    dataset.drop('News_headline', axis=1, inplace=True)
    dataset = dataset[['News', 'Category']]
    dataset = dataset[pd.notnull(dataset['News'])]
    
    sizes = dataset.groupby('Category').size()
    print(sizes)
    summ = 0
    for size in sizes:
        if size < 2000:
            summ += size
    counter = 14127 - summ // 5
    for index, row in dataset[dataset['Category'] == 'politics'].iterrows():
        if counter:
            dataset.drop(index, inplace=True)
            counter -= 1
    print(dataset.groupby('Category').size())

    # length = len(dataset)
    # test_size = length // 4
    # train_size = length - test_size
    # dataset = dataset.sample(frac=1)
    # test_dataset = dataset.head(test_size)
    # train_dataset = dataset.tail(train_size)
    dataset.to_csv('train.csv')