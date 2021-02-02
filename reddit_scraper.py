import praw
import pandas as pd
import datetime as dt


'''
link utili:
https://datatofish.com/pandas-dataframe-to-sql/
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python
'''
class SReddit():
    def __init__(self, subreddit, limit, keywords, d=None):
        if d is None:
            d = {}
        self.subreddit = subreddit
        self.limit = limit
        self.keywords = keywords
        self.d = d


    def scraper(self):
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

        return self.d

    def to_csv(self):
        '''
        per creare direttamente il file .csv
        :return: dataframe pandas
        '''
        df = pd.DataFrame(self.d)
        df.to_csv('REDDIT.csv', index=False)
        return df

    def frequency(self):
        '''
        per calcolare il numero di volte che una o più keyword viene nominata
        :return:
        '''
        df = pd.DataFrame(self.d)
        titoli = df['title']

        keywords = self.keywords

        temp=0

        for i in titoli:
            for j in i.split():
                for k in keywords:
                    if j==k:
                        temp+=1

        return temp



#prova del codice
Sreddit = SReddit('wallstreetbets', 100, ['GME', 'BTC'])

Sreddit.scraper()

Sreddit.frequency()