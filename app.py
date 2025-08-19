import streamlit as st
from fontTools.varLib.mutator import percents
from wordcloud import WordCloud
import preprocessor, helper
import matplotlib.pyplot as plt

from helper import most_common_words, daily_timeline

st.sidebar.title("Whatsapp Chat Analyzer")

uploaded_file = st.sidebar.file_uploader("Upload a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df  = preprocessor.preprocess(data)


    # unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"All Users Chats")

    selected_user = st.sidebar.selectbox("show analysis wrt", user_list)

    if st.sidebar.button("Analyze Chats"):

        num_msgs, words, num_media_msgs, num_links = helper.fetch_stats(selected_user,df)
        st.title("Chat Statics")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("No. of Msges")
            st.title(num_msgs)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("No. Media Messages")
            st.title(num_media_msgs)
        with col4:
            st.header("No. of Links")
            st.title(num_links)
    # TimeLine
    st.title('Mothly Time Line')
    timeline = helper.monthly_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(timeline['time'], timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)


    st.title('Daily Timeline')
    daily_timeline = helper.daily_timeline(selected_user, df)
    fig, ax = plt.subplots()
    ax.plot(daily_timeline['only_date'], daily_timeline['message'])
    plt.xticks(rotation='vertical')
    st.pyplot(fig)

    # most active user in chat
    if selected_user == "All Users Chats":
        st.title("Most Active User")
        x, percents_df = helper.most_active_users(df)
        fig, ax = plt.subplots()

        col1, col2 = st.columns(2)

        with col1:
            ax.bar(x.index, x.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        with col2:
            st.dataframe(percents_df)

    # wordcloud
    df_wc = helper.create_wordcloud(selected_user, df)
    fig, ax = plt.subplots()
    ax.imshow(df_wc)
    st.pyplot(fig)


    most_common_words_df = helper.most_common_words(selected_user, df)

    fig, ax = plt.subplots()
    ax.barh(most_common_words_df[0],most_common_words_df[1])
    plt.xticks(rotation='vertical')
    st.title('Most Used Words')
    st.pyplot(fig)



    # emojis
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most used emojis")
        most_common_emojis = helper.most_used_emojis(selected_user, df)
        fig, ax = plt.subplots()
        ax.pie(
            most_common_emojis['count'],
            labels=most_common_emojis['emoji'],
            autopct='%1.1f%%',
            startangle=140,
            pctdistance=0.85,  # Moves percentage labels inward
            labeldistance=1.1  # Moves emoji labels outward
        )
        ax.set_title('Most used emojis')
        st.pyplot(fig)

    with col2:
        st.subheader("Top Emojis Table")
        st.dataframe(most_common_emojis)