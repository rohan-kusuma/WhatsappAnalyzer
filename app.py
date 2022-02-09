import streamlit as st
import preprocessor
import re
import pandas
import stats
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import numpy as np


st.sidebar.title('Whatsapp Chat Analyzer')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    if data.startswith('['):
        df = preprocessor.iosdata(data)
    else:
        df = preprocessor.androiddata(data)

    # fetch all users
    user_list = df.user.unique().tolist()
    if 'group_message' in user_list:
        user_list.remove('group_message')

    user_list.sort()
    user_list.insert(0, 'overall')
    user_selected = st.sidebar.selectbox('show analysis', user_list)

    if st.sidebar.button('show analysis'):
        st.header('Chat statistics')
        col1, col2, col3, col4 = st.columns(4)
        num_messages, word_len, media_msg, emojis_sent = stats.fetch_stats(user_selected, df)

        with col1:
            st.write('Messages Sent')
            st.title(num_messages)
        with col2:
            st.write('Total words')
            st.title(word_len)
        with col3:
            st.write('Media shared')
            st.title(media_msg)
        with col4:
            st.write('Emojis Sent')
            st.title(emojis_sent)
        st.markdown('-' * 70)

        # Fetch user statistics
        if user_selected == 'overall':
            st.header('User Statistics')

            top_user, all_users, msg_top_sent, top_msg, average_msgs = stats.most_busy_users(df)
            col1, col2, col3= st.columns(3)

            with col1:
                st.write('Total Users')
                st.title(all_users)

            with col2:
                st.write('Top User')
                st.title(top_user)
            with col3:
                st.write('messages sent by top user')
                st.title(msg_top_sent)

            col1 = st.columns(1)
            st.write('Most busy users')
            fig = plt.figure(figsize=(10, 4))
            plt.xticks(rotation=80)
            plt.title('Most busy users')
            sns.barplot(x="user", y="messages", data=top_msg)
            st.pyplot(fig)
            st.markdown('-' * 70)

        st.header('Emojis Analysis')
        common_emojis, unique_emojis,em,len_of_most_common = stats.emoji_helper(user_selected,df)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write('Most common emoji')
            st.title(common_emojis)


        with col2:
            st.write('No.of times common emoji used')
            st.title(len_of_most_common)

        with col3:
            st.write("Different emojis used")
            st.title(unique_emojis)

        col4 = st.columns(1)
        fig = px.pie(values=em['count'], labels=em['emoji'],names=em['emoji'],title='Top 5 Emojis Used' )
        fig.update_traces(textposition='inside', textinfo='percent+label')
        st.plotly_chart(fig)
        st.markdown("-"*50)

        st.title('Timeline Analysis')
        hourly,weekly = stats.monthly_weekly_time(user_selected,df)

        col1,col2 = st.columns(2)
        with col1:
            st.header('Busy Hour')
            st.write(hourly['hours_p'][0])
        with col2:
            st.header('Busy weekday')
            st.write(weekly['weekname'][0])

        st.header('Activity by Hour')
        fig = plt.figure(figsize=(15, 8))
        plt.xticks(rotation=80)
        plt.title('Activity by Hour')
        sns.barplot(x="hours_p", y="messages", data=hourly)
        st.pyplot(fig)


        st.header('Activity by Weekday')
        fig = plt.figure(figsize=(10, 4))
        plt.xticks(rotation=80)
        plt.title('Activity by weekday')
        sns.barplot(x="weekname", y="messages", data=weekly)
        st.pyplot(fig)

        timeline = stats.timeline_chart(user_selected,df)
        st.header('Monthly Timeline')
        fig = plt.figure(figsize=(15, 8));
        plt.plot(timeline['time'], timeline['count'])
        plt.xticks(rotation=90)
        st.pyplot(fig)
        st.markdown("-" * 50)

        st.title('Words')
        wordcloud = stats.create_wordcloud(user_selected, df)
        st.header('WordCloud')
        fig, ax = plt.subplots()
        fig.set_figheight(5)
        fig.set_figwidth(10)
        plt.axis('off')
        ax.imshow(wordcloud, aspect='auto')
        st.pyplot(fig)


















