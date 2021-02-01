import praw
import pandas as pd
import datetime as dt


'''
link utili:
https://datatofish.com/pandas-dataframe-to-sql/
https://www.kite.com/python/answers/how-to-insert-the-contents-of-a-csv-file-into-an-sqlite3-database-in-python
'''
'''
App Name: WSBscraper 
App ID: z2edaKf81OaY2w 
'''

reddit = praw.Reddit(client_id='z2edaKf81OaY2w',
                     client_secret='ZgEG_HottISxIa27_UlXipTDY8j-vA',
                     user_agent='WSBscraper',
                     username='Logical_Delivery8331',
                     password='070719981998aA%#[]')

subreddit = reddit.subreddit('wallstreetbets')
new_sub = subreddit.new(limit = 100)


d = {'author':[], 'title':[], 'body':[], 'id':[], 'comments':[]}


for submission in new_sub:
    d['author'].append(submission.author)
    d['body'].append(submission.selftext)
    d['title'].append(submission.title)
    d['id'].append(submission.id)
    d['comments'].append(submission.comments)

df = pd.DataFrame(d)

df.to_csv('REDDIT.csv')

titoli = df['title']

keywords = ['GME']

temp=0

for i in titoli:
    for j in i.split():
        for k in keywords:
            if j==k:
                temp+=1

print(temp)

