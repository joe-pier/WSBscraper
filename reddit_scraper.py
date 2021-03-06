import os
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
import nltk
#nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer

class SReddit():
    '''
    class SReddit
    '''

    def __init__(self, subreddit, limit, keywords, posts=None, keywords_dict=None, count=None):
        if count is None:
            count = {}
        if keywords_dict is None:
            keywords_dict = {}
        if posts is None:
            posts = {}
        self.subreddit = subreddit
        self.limit = limit
        self.keywords = keywords
        self.posts = posts
        self.keywords_dict = keywords_dict
        self.count = count
        self.test = {}

    def scraper(self, tocsv=False):
        '''
        scraping of subredit definited in the object 
        '''
        ### FILL IN WITH YOUR REDDIT ACCOUNT USERNAME  ###

        usr = 'YOU REDDIT USERNAME'

        # check if the password and username are empty
        if (not usr) and (not psw):
            return False

        reddit = praw.Reddit(client_id='hvUkZg4M5VRv_g',
                             client_secret='GsV8Dnr1M8nwV0-3YTvIedlSE0yAaQ',
                             user_agent='RScraper',
                             username=usr)

        subreddit = reddit.subreddit(self.subreddit)
        new_sub = subreddit.new(limit=self.limit)
        # create the struct of the posts dictonary
        self.posts = {'time': [], 'upvotes': [], 'title': [], 'body': []}
        # add posts
        for submission in new_sub:
            self.posts['time'].append(submission.created_utc)
            self.posts['upvotes'].append(submission.score)
            self.posts['body'].append(submission.selftext)
            self.posts['title'].append(submission.title)
            # self.posts['id'].append(submission.id)
            # self.posts['comments'].append(submission.comments)
            # self.posts['author'].append(submission.author)
        # convert to CSV?
        if tocsv == True:
            to_csv(self.posts, 'exemples/REDDIT', header=True, )

        return self.posts

    def frequency(self, tocsv=False):
        '''
        for calculate the number of times of the keyword it's nominated 
        :return: dictionary
        '''
        df = pd.DataFrame(self.posts)
        title = df['title']

        keywords = self.keywords

        self.keywords_dict = dict.fromkeys(keywords, 0)
        for i in title:
            for j in i.split():
                for k in self.keywords_dict.keys():
                    if j == k:
                        self.keywords_dict[k] += 1
                        if k not in self.test.keys():
                            self.test[k] = [i]

                        else:
                            self.test[k] += [i]
        if tocsv == True:
            to_csv([self.keywords_dict], 'exemples/FREQUENCE', header=self.keywords)
            to_csv([self.test], 'exemples/TEST', header=self.keywords)

        return self.keywords_dict

    def top__used_words(self, tocsv=False, plot_=False, WordCloud_=False, CloudDimension=100,
                        output_img='RedditWordCloud'):
        '''
        most used words
        :return:
        '''

        items = self.posts['title']
        conc_items = '\n'.join(items)
        conc_ = conc_items.split(' ')

        # is a dictonary
        self.count = Counter(conc_)

        excluded_words = ['The', 'the', 'a', 'my', 'all', 'with', 'is', 'this', 'The', 'A', 'All', 'To', 'to', 'just',
                          'and', 'you', 'are', 'at', 'on', 'in', 'if', 'it', 'when', 'while', 'I', 'what', 'have',
                          'got', 'but', 'up', 'for', 'more', 'we', 'can', 'THE', 'i'
            , 'of', 'me', 'only', '-', 'YOU', 'be', 'that', 'or', 'about', 'from', 'still', 'out','so','do', 'their', 'has', 'some','TO']

        for i in excluded_words: del self.count[i]

        sorted_count = sorted(self.count.items(), key=itemgetter(1), reverse=True)
        # list containing in order the most used words excluding the useless words
        X, Y = [*zip(*sorted_count)]
        if tocsv == True:
            to_csv(sorted_count, 'exemples/TOP_USED_WORDS', header=['WORD', 'OCCURRENCES'])

        if plot_ == True:
            plt.bar(X, Y)
            plt.show()

        if WordCloud_ == True:
            # to use wordcloud with online image
            # mask_image = 'https://image.flaticon.com/icons/png/512/52/52191.png'
            # mask = np.array(Image.open(
            # requests.get(mask_image, stream=True).raw))
            # to use wordlcloud with local image

            # image to use with worldcloud
            img = "wordcloud/reddit_logo.png"
            mask = np.array(Image.open(img))

            wordcloud = WordCloud(background_color="white", max_words=CloudDimension, mask=mask, contour_width=0,
                                  contour_color='black', width=800, height=800, colormap='inferno',
                                  font_path='wordcloud/Helvetica Neu Bold.ttf')

            wordcloud.generate(' '.join(X))
            plt.figure(figsize=(5, 5))
            plt.imshow(wordcloud, interpolation='bilinear')
            plt.axis("off")

            plt.savefig('exemples/' + output_img)
            plt.show()
        return sorted_count

    def hottest_ones(self, tocsv=False):
        '''
        attempt to catch the best reddit posts that are likely to become the top ones
        the greater the number of upvotes and the shorter the time from which it was written the higher will be its "hot_ratio"
        :return:
        '''

        title = self.posts['title']
        upvotes = self.posts['upvotes']
        time_ = self.posts['time']
        DateTime = [datetime.utcfromtimestamp(f).strftime('%Y-%m-%d %H:%M:%S') for f in time_]
        actual_time = time.time()

        Delta_time = [-temp + actual_time for temp in time_]
        hot_ratio = [a / b for a, b in zip(upvotes, Delta_time)]

        lista = list(zip(DateTime, title, hot_ratio))

        sorted_lista = sorted(lista, key=itemgetter(2), reverse=True)

        if tocsv == True:
            to_csv(sorted_lista, 'exemples/HOTTEST_ONES', header=['time', 'post', 'hot ratio'])

        return sorted_lista


    def naive_count(self, graph = False):
        import re
        import string
        from nltk.tokenize import word_tokenize
        from collections import Counter
        #print(self.posts['title'])

        tokens = []

        for text in self.posts['title']:
            text_no_numbers_no_punctuation = re.sub("[^-9A-Za-z ]", '', text)
            text_no_upper_case = "".join([i.lower() for i in text_no_numbers_no_punctuation if i not in string.punctuation])
            text_tokenized = word_tokenize(text_no_upper_case)

            tokens += text_tokenized
            #print(text_tokenized)

        naive_counts = Counter(tokens)


        return naive_counts

    def general_sentiment(self):
        data = pd.read_csv('exemples/REDDIT.csv')
        pd_data = pd.DataFrame(data)
        col_name = list(data)
        m = len(pd_data)

        total = 0
        for i in range(0, m):
            sentence = data[col_name[2]][i]
            sid = SentimentIntensityAnalyzer()
            test = sid.polarity_scores(sentence)
            # print(f'{sentence} = {test}')
            total += test['compound']
        return total

    def specific_sentiment(self):
        '''

        :return:
        '''

        data = self.test
        dizionario = {}
        for i in self.keywords:
            #print(i)
            total_=0
            for sentence_ in data[i]:
                sid = SentimentIntensityAnalyzer()
                test = sid.polarity_scores(sentence_)
                total_ += test['compound']
                #print(total_)
            dizionario[i]=total_

        return dizionario



def to_csv(d, name, header=None, index=False):
    '''
    the input is a dictonary
    for create a csv file
    :return: dataframe pandas
    '''
    df = pd.DataFrame(d)
    df.to_csv(name + '.csv', header=header, index=index)
    return df





if __name__ == "__main__":
    # insert here your keywords
    key_words = ['GME', 'MVIS']
    # insert here the subreddit
    sub_reddit = 'wallstreetbets'
    # insert here the limit of posts
    limit = 100
    Sreddit = SReddit(sub_reddit, limit, key_words)
    if (not Sreddit.scraper(tocsv=True)):
        print("PLEASE fill in with your reddit username")
        os._exit(-1)


    mark = Sreddit.general_sentiment()
    print(mark)

    frequence = Sreddit.frequency(tocsv=True)
    #print(Sreddit.test)

    test = Sreddit.specific_sentiment()

    from time import gmtime, strftime
    tempo = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    test['time'] = tempo
    print(test)
    dati = pd.DataFrame([test])
    dati.set_index('time', inplace=True)
    dati.to_csv('results/RISULTATI.csv', mode = 'a')



    #Sreddit.naive_count(graph=True)
    #top_words = Sreddit.top__used_words(tocsv=False, plot_=False, WordCloud_=False, CloudDimension=100)
    #hot_ratio = Sreddit.hottest_ones(tocsv=False)
