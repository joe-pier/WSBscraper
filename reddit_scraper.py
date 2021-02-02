import time
from collections import Counter
from datetime import datetime
from operator import itemgetter
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import praw
from PIL import Image
from wordcloud import WordCloud

'''
link utili:
https://datatofish.com/pandas-dataframe-to-sql/
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python
'''


class SReddit():
    '''
    classe SReddit
    '''

    def __init__(self, subreddit, limit, keywords, d=None, keywords_dict=None, count=None):
        if count is None:
            count = {}
        if keywords_dict is None:
            keywords_dict = {}
        if d is None:
            d = {}
        self.subreddit = subreddit
        self.limit = limit
        self.keywords = keywords
        self.d = d
        self.keywords_dict = keywords_dict
        self.count = count

    def scraper(self, tocsv=False):
        '''
        scraping del subreddit definito nell'oggetto
        :return: dizionario
        '''

        reddit = praw.Reddit(client_id='z2edaKf81OaY2w',
                             client_secret='ZgEG_HottISxIa27_UlXipTDY8j-vA',
                             user_agent='WSBscraper',
                             username='',
                             password='')
        # NB. il codice funziona se viene messa la propria password e nome utente in username e password.
        subreddit = reddit.subreddit(self.subreddit)
        new_sub = subreddit.new(limit=self.limit)

        self.d = {'time': [], 'upvotes': [], 'title': [], 'body': []}

        for submission in new_sub:
            self.d['time'].append(submission.created_utc)
            self.d['upvotes'].append(submission.score)
            self.d['body'].append(submission.selftext)
            self.d['title'].append(submission.title)
            # self.d['id'].append(submission.id)
            # self.d['comments'].append(submission.comments)
            # self.d['author'].append(submission.author)

        if tocsv == True:
            to_csv(self.d, 'REDDIT')
        return self.d

    def frequency(self, tocsv=False):
        '''
        per calcolare il numero di volte che una o più  keyword viene nominata
        per trasformarlo in un .csv basta usare la funzione to_csv
        :return: dictionary
        '''
        df = pd.DataFrame(self.d)
        titoli = df['title']

        keywords = self.keywords

        self.keywords_dict = dict.fromkeys(keywords, 0)

        for i in titoli:
            for j in i.split():
                for k in self.keywords_dict.keys():
                    if j == k:
                        self.keywords_dict[k] += 1
        if tocsv == True:
            to_csv([self.keywords_dict], 'FREQUENZE', header=self.keywords)

        return self.keywords_dict

    def top__used_words(self, tocsv=False, plot_=False, WordCloud_=False, CloudDimension=100):
        '''
        parole più utilizzate
        :return:
        '''

        items = self.d['title']

        conc_items = '\n'.join(items)
        conc_ = conc_items.split(' ')

        # è un dizionario
        self.count = Counter(conc_)

        excluded_words = ['The', 'the', 'a', 'my', 'all', 'with', 'is', 'this', 'The', 'A', 'All', 'To', 'to', 'just',
                          'and', 'you', 'are', 'at', 'on', 'in', 'if', 'it', 'when', 'while', 'I', 'what', 'have',
                          'got', 'but', 'up', 'for', 'more', 'we', 'can', 'THE', 'i'
                            ,'of', 'me', 'only', '-', 'YOU', 'be', 'that']

        for i in excluded_words: del self.count[i]

        sorted_count = sorted(self.count.items(), key=itemgetter(1), reverse=True)
        # lista contenente in ordine le parole più usate escluse le parole inutili


        X, Y = [*zip(*sorted_count)]

        if tocsv == True:
            to_csv(sorted_count, 'TOP USED WORDS', header=['WORD', 'OCCURRENCES'])

        if plot_ == True:
            plt.bar(X, Y)
            plt.show()

        if WordCloud_ == True:
            # to use wordcloud with online image
            # mask_image = 'https://image.flaticon.com/icons/png/512/52/52191.png'
            # mask = np.array(Image.open(
            # requests.get(mask_image, stream=True).raw))

            # to use wordlcloud with local image
            mask = np.array(Image.open("img.png"))

            wordcloud = WordCloud(background_color="white", max_words=CloudDimension, mask=mask, contour_width=0,
                                  contour_color='black', width=400, height=400)
            wordcloud.generate(' '.join(X))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")
            plt.show()

        return sorted_count


    def hottest_ones(self, tocsv=False):
        '''
        attempt to catch the best reddit posts that are likely to become the top ones

        tanto maggiore è il numero di upvotes e tanto minore è il tempo dal quale è stato scritto tanto più alto sarà il suo "hot_ratio"
        :return:
        '''

        title = self.d['title']
        upvotes = self.d['upvotes']
        time_ = self.d['time']
        DateTime = [datetime.utcfromtimestamp(f).strftime('%Y-%m-%d %H:%M:%S') for f in time_]
        actual_time = time.time()

        Delta_time = [-temp + actual_time for temp in time_]
        hot_ratio = [a / b for a, b in zip(upvotes, Delta_time)]

        lista = list(zip(DateTime, title, hot_ratio))

        sorted_lista = sorted(lista, key=itemgetter(2), reverse=True)

        if tocsv == True:
            to_csv(sorted_lista, 'HOTTEST ONES', header=['time', 'post', 'hot ratio'])

        return sorted_lista


def to_csv(d, name, header=None, index=False):
    '''
    input è un dizionario.
    per creare direttamente il file .csv
    :return: dataframe pandas
    '''
    df = pd.DataFrame(d)
    df.to_csv(name + '.csv', header=header, index=index)
    return df


# prova del codice#


Sreddit = SReddit('wallstreetbets', 1500, ['GME', 'BTC', 'silver', '$GME'])

Sreddit.scraper(tocsv=True)

frequenze = Sreddit.frequency(tocsv=True)

top_words = Sreddit.top__used_words(tocsv=True, plot_=False, WordCloud_=True, CloudDimension=1000)

hot_ratio = Sreddit.hottest_ones(tocsv=True)
