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

data = []

if chat_file:
    bytes_data = chat_file.getvalue().decode('utf-8').splitlines()
    st.write(len(bytes_data))

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


#     with open(bytes_data, encoding="utf-8") as fp:
#         fp.readline()
#         messageBuffer = []
#         date, time, author = None, None, None
#         while True:
#             line = fp.readline()
#             if not line:
#                 break
#             line = line.strip()
#             if date_time(line):
#                 if len(messageBuffer) > 0:
#                     data.append([date, time, author, ' '.join(messageBuffer)])
#                 messageBuffer.clear()
#                 date, time, author, message = getDatapoint(line)
#                 messageBuffer.append(message)
#             else:
#                 messageBuffer.append(line)

chat_df = pd.DataFrame(data, columns=["Date", 'Time', 'Author', 'Message'])
chat_df['Date'] = pd.to_datetime(chat_df['Date'])

st.dataframe(chat_df)