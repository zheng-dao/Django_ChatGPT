from django.conf import settings
settings.configure()
import pickle
import config
import argparse
from nltk_functions import predict_category, scrape_url, url_parse_request
import os, csv

def save_csv(rows=[], header=[], fn='temp.csv', fp='app/data/rpt', mode='w'):
    with open(os.path.join(fp, fn), mode, newline='') as outfile:
        wcsv = csv.writer(outfile, delimiter=',')
        if header:
            wcsv.writerow(header)
        for r in rows:
            wcsv.writerow(r)

def opentxt(fn='cu_words.txt', fp='app/data/keywords', mode='r'):
    rows = []
    with open(os.path.join(fp, fn)) as f:
        for line in f:
            rows.append(line.strip())
    return rows

if __name__ == '__main__':
    pickle_in = open(config.WORDS_FREQUENCY_PATH, "rb")
    words_frequency = pickle.load(pickle_in)

    parser = argparse.ArgumentParser(description='URLs for category predictions')
    parser.add_argument('-u', '--url', help='Predict custom website')
    parser.add_argument('-t', '--text_file_path', help='Predict websites written in text file')
    parser.add_argument('-m', '--url_only', help='Predict only the url')

    args = parser.parse_args()
    rows = []
    i = 0
    if args.url_only:
        file_path = args.text_file_path
        words = opentxt()
        with open(file_path) as f:
            for url in f:
                print(i)
                url = url.replace('\n', '')
                tokens_lemmatize = url_parse_request(url, words=words)
                results = predict_category(words_frequency, tokens_lemmatize)
                if results:
                    rows.append([results[0], results[2], url, str(tokens_lemmatize)])
                    print('Predictions 1 and 2:', results[0], '|', results[2], '|', url)
                    print('----------------------------------------------------------------------')
                    save_csv(rows, ['cat', 'cat2', 'url', 'tokens'], mode='a')
                i += 1
    else:
        if args.url:
            url = args.url
            print(url)
            results = scrape_url(url, words_frequency)
            if results:
                print('Predicted main category:', results[0])
                print('Predicted submain category:', results[2])
        elif args.text_file_path:
            file_path = args.text_file_path
            with open(file_path) as f:
                for url in f:
                    url = url.replace('\n', '')
                    print(url)
                    results = scrape_url(url.replace('\n', ''), words_frequency)
                    if results:
                        print('Predicted main category:', results[0])
                        print('Predicted submain category:', results[2])
        else:
            parser.error("Please specify websites input type. More about input types you can find 'python predict_url -h'")
