import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
from neattext import TextExtractor
from collections import Counter
import pandas as pd
import emoji
import plotly.express as px


def fetch_stats(user, df):
    if user != 'overall':
        df = df[df['user'] == user]
    num_messages = df.shape[0]


    media_msg = df[df['messages'].str.contains('image omitted|Image Omitted') | df['messages'].str.contains(
        'media omitted|Media omitted')].shape[0]
    words = []
    for message in df['messages']:
        words.extend(message.split())


    emojis = []
    for message in df['messages']:
        sent = TextExtractor(message)

        emojis.append(sent.extract_emojis())

    df['emojis'] = emojis
    emojis_sent = sum(df['emojis'].str.len())

    return num_messages, len(words), media_msg, emojis_sent


def most_busy_users(df):
    all_users = len(df['user'].unique())
    top_msg = df.groupby('user')['messages'].count().sort_values(ascending=False).head(10).reset_index()
    top_user = top_msg['user'][0]
    msg_top_sent = top_msg['messages'][0]
    average_msgs = len(df['messages'])/len(df['user'].unique())
    return top_user, all_users, msg_top_sent, top_msg, average_msgs

def emoji_helper(user,df):
    if user!= 'overall':
        df = df[df['user'] == user]
    emojis = []
    for message in df['messages']:
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])
    emoji_df = pd.DataFrame(Counter(emojis).most_common(20))
    emoji_df.columns = ['emoji', 'count']
    most_common_emoji = emoji_df['emoji'][0]
    len_most_common = emoji_df['count'][0]
    unique_emojis = len(emoji_df['emoji'].unique())

    em = emoji_df.head(5)
    return most_common_emoji,unique_emojis,em,len_most_common

def monthly_weekly_time(user,df):
    if user != 'overall':
        df = df[df['user'] == user]
    weekly= df.groupby('weekname')['messages'].size().reset_index().sort_values(by ='messages',ascending=False).reset_index()
    hourly = df.groupby('hour')['messages'].count().reset_index().sort_values(by ='messages',ascending=False).reset_index()
    hours_p = []
    for h in hourly['hour']:
        if h > 12:
            hours_p.append(str(h - 12) + " " + "PM")
        else:
            hours_p.append(str(h) + " " + "AM")
    hourly['hours_p'] = hours_p
    hourly[['hours_p', 'messages']]
    return hourly,weekly


def timeline_chart(user, df):
    if user != 'overall':
        df = df[df['user'] == user]
    timeline = df.groupby(['year', 'month']).size().reset_index(name='count')
    year_month = []
    for i in range(timeline.shape[0]):
        year_month.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = year_month
    return timeline

def create_wordcloud(user, df):
    if user != 'overall':
        df = df[df['user'] == user]
    wc = WordCloud(stopwords=STOPWORDS, width=500, height=500, min_font_size=10, background_color='white')
    df_wc = wc.generate(df['messages'].str.cat(sep=' '))



    return df_wc



