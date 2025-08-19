from urlextract import URLExtract
from wordcloud import WordCloud
import pandas as pd
from collections import Counter
import emoji
import nltk
from nltk.corpus import stopwords


extract = URLExtract()

def fetch_stats(selected_user,df):
    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]
    num_msgs = df.shape[0]

    words = []
    for msg in df['message']:
        words.extend(msg.split())

    num_media_msgs = df[df['message'].str.strip() == '<Media omitted>'].shape[0]

    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_msgs, len(words), num_media_msgs, len(links)

def most_active_users(df):
    x = df['user'].value_counts().head()
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2).reset_index().rename(
        columns={'user': 'name', 'count': 'percent'})
    return x, df

def create_wordcloud(selected_user,df):

    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]
    wc = WordCloud(width=500, height=500, background_color='white', min_font_size=10)
    df_wc = wc.generate(df['message'].str.cat(sep=' '))

    return df_wc


# Base stopwords
stop_words = set(stopwords.words('english'))

# Add your custom stopwords
custom_words = {'ok', 'hmm', 'haha', 'yes', 'no', 'media', 'deleted', 'message','chhe','..','che','j','ne','thi','ae','chu','na','?','.','hu','ha','ni','e','tu','hoi'}
stop_words.update(custom_words)
def remove_stopwords(text):
    words = text.split()
    filtered = [word for word in words if word.lower() not in stop_words]
    return ' '.join(filtered)

def most_common_words(selected_user,df):
    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'System']
    temp = temp[temp['message'].str.strip() != '<Media omitted>']
    temp['message'] = temp['message'].apply(remove_stopwords)
    words = []
    for message in temp['message']:
        words.extend(message.split())

    most_common_words_df = pd.DataFrame(Counter(words).most_common(10))

    return most_common_words_df

def most_used_emojis(selected_user,df):
    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    emoji_freq = Counter(emojis)
    top_emojis = emoji_freq.most_common(5)
    emoji_df = pd.DataFrame(top_emojis, columns=['emoji', 'count'])

    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year','month_num' ,'month']).count()['message'].reset_index()
    time = []
    for i in range(timeline.shape[0]):
        time.append(str(timeline['month'][i]) + "-" + str(timeline['year'][i]))
    timeline['time'] = time

    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'All Users Chats':
        df = df[df['user'] == selected_user]
    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline