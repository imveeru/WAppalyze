import pandas as pd
import re

# Split the chat string by newline characters and process line by line
def txt_to_df(chat_string):
    # Regular expression pattern for matching lines in the chat
    pattern = re.compile(r'(\d{1,4}/\d{1,2}/\d{2,4}, \d{1,2}:\d{1,2}) - (.*?): (.*)')

    # Lists to hold the extracted details
    dates = []
    times = []
    senders = []
    messages = []

    for line in chat_string.strip().split('\n'):
        match = pattern.match(line)
        if match:
            date_time, sender, message = match.groups()
            date, time = date_time.split(', ')
            dates.append(date)
            times.append(time)
            senders.append(sender)
            messages.append(message)

    return pd.DataFrame(
        {'Date': dates, 'Time': times, 'Author': senders, 'Message': messages}
    )

