import praw
import pandas as pd
import datetime as dt
from collections import Counter

'''
link utili:
https://datatofish.com/pandas-dataframe-to-sql/
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python
'''
class SReddit():
    def __init__(self, subreddit, limit, keywords, d=None, keywords_dict=None, count=None):
        if count is None:
            count = {}
        if keywords_dict is None:
            keywords_dict={}
        if d is None:
            d = {}
        self.subreddit = subreddit
        self.limit = limit
        self.keywords = keywords
        self.d = d
        self.keywords_dict= keywords_dict

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
        #NB. il codice funziona se viene messa la propria password e nome utente in username e password.
        subreddit = reddit.subreddit(self.subreddit)
        new_sub = subreddit.new(limit = self.limit)


        self.d = {'time':[], 'author':[], 'title':[], 'body':[], 'id':[], 'comments':[]}


        for submission in new_sub:
            self.d['time'].append(dt.datetime.now())
            self.d['author'].append(submission.author)
            self.d['body'].append(submission.selftext)
            self.d['title'].append(submission.title)
            self.d['id'].append(submission.id)
            self.d['comments'].append(submission.comments)

        if tocsv==True:
            to_csv(self.d, 'REDDIT')
        return self.d


    def frequency(self, tocsv =False):
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
                    if j==k:
                        self.keywords_dict[k]+=1
        if tocsv ==True:
            to_csv([self.keywords_dict], 'FREQUENZE')

        return [self.keywords_dict]


    def top__used_words(self, tocsv = False):
        '''
        parole più utilizzate, bisogna escludere quelle inutili come the of o to
        :return:
        '''

        items = self.d['title']

        conc_items = '\n'.join(items)
        conc_ = conc_items.split(' ')
        self.count = Counter(conc_)

        if tocsv == True:
            to_csv([self.count], 'TOP USED WORDS')
        return self.count



def to_csv(d, name ):
    '''
    input è un dizionario.
    per creare direttamente il file .csv
    :return: dataframe pandas
    '''
    df = pd.DataFrame(d)
    df.to_csv(name+'.csv')
    return df




#prova del codice#


Sreddit = SReddit('wallstreetbets', 5, ['GME', 'BTC', 'COMEX', 'iShare'])

posts = Sreddit.scraper(tocsv=True)

frequenze = Sreddit.frequency(tocsv=True)

top_words = Sreddit.top__used_words(tocsv=True)
