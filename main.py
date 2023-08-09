import streamlit as st

st.set_page_config(
    page_title="WAppalyze",
    page_icon="💬",
    initial_sidebar_state="expanded",
)

#hide streamlit default
hide_st_style ='''
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html=True)

st.title("💬WAppalyze")

with st.sidebar:
    chat_file=st.file_uploader("Upload your Whatsapp Chat file.")

from helper import *
import pandas as pd
import numpy as np
from collections import Counter

data = []

if chat_file:
    bytes_data = chat_file.getvalue().decode('utf-8').splitlines()

    messageBuffer = []
    date, time, author = None, None, None
    for line in bytes_data:
        if not line:
            break
        line = line.strip()
        if date_time(line):
            if messageBuffer:
                data.append([date, time, author, ' '.join(messageBuffer)])
            messageBuffer.clear()
            date, time, author, message = getDatapoint(line)
            messageBuffer.append(message)
        else:
            messageBuffer.append(line)

    chat_df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
    chat_df['Date'] = pd.to_datetime(chat_df['Date'])
    chat_df = chat_df[chat_df.Author.notnull()]

    #st.dataframe(chat_df)
    media_messages = chat_df[chat_df["Message"]=='<Media omitted>']

    st.markdown("### 📨 Total Messages")
    st.write(chat_df.shape[0])
    st.divider()

    authors=chat_df.Author.unique()
    st.markdown("### 👥C hat Participants:")
    st.write(authors)
    st.divider()

    chat_df['emoji'] = chat_df["Message"].apply(split_count)
    chat_df['Letter_Count'] = chat_df['Message'].apply(lambda s : len(s))
    chat_df['Word_Count'] = chat_df['Message'].apply(lambda s : len(s.split(' ')))

    msg_count=[]
    wpms=[]
    ws=[]
    mms=[]
    emojis=[]

    for author in authors:
        author_df=chat_df[chat_df.Author == author]
        msg_count.append(author_df.shape[0])
        ws.append(int(np.sum(author_df["Word_Count"])))
        wpms.append(int(np.sum(author_df["Word_Count"])/author_df.shape[0]))
        mms.append(author_df[author_df["Message"]=='<Media omitted>'].shape[0])
        emojis.append(sum(author_df['emoji'].str.len()))

    data_df=pd.DataFrame({
        "Authors":authors,
        "Messages Sent":msg_count,
        "Words Sent":ws,
        "Average Words per message":wpms,
        "Multimedia Shared":mms,
        "Emojis Sent":emojis
    })

    st.dataframe(data_df)

    total_emojis_list = [a for b in chat_df.emoji for a in b]
    emoji_dict = dict(Counter(total_emojis_list))
    emoji_dict = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)

    emoji_df = pd.DataFrame(emoji_dict, columns=['emoji', 'count'])

    st.dataframe(emoji_df)