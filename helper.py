import regex
import emoji
from datetime import datetime
import plotly.express as px
import pandas as pd

def date_time(s):
    pattern = '^([0-9]+)(\/)([0-9]+)(\/)([0-9]+), ([0-9]+):([0-9]+)[ ]?(AM|PM|am|pm)? -'
    result = regex.match(pattern, s)
    return bool(result)

def find_author(s):
    s = s.split(":")
    return len(s) == 2

def getDatapoint(line):
    splitline = line.split(' - ')
    dateTime = splitline[0]
    date, time = dateTime.split(", ")
    message = " ".join(splitline[1:])
    if find_author(message):
        splitmessage = message.split(": ")
        author = splitmessage[0]
        message = " ".join(splitmessage[1:])
    else:
        author= None
    return date, time, author, message

def split_count(text):
    emoji_list = []
    data = regex.findall(r'\X',text)
    for word in data:
        if any(char in emoji.UNICODE_EMOJI_ENGLISH for char in word):
            emoji_list.append(word)
    return emoji_list

def count_frequency(arr):
    frequency = {}
    
    for element in arr:
        if element in frequency:
            frequency[element] += 1
        else:
            frequency[element] = 1
            
    return frequency

def sort_dates(date_list):
    date_objects = [datetime.strptime(date, "%m/%d/%y") for date in date_list]
    sorted_dates = sorted(date_objects)
    return [date.strftime("%m/%d/%y") for date in sorted_dates]

def change_date_format(date_list):
    new_format = "%m/%d/%y"
    new_dates = []
    for date_str in date_list:
        try:
            original_date = datetime.strptime(date_str, new_format)
            new_date_str = original_date.strftime(new_format)
            new_dates.append(new_date_str)
        except ValueError:
            print(f"Error parsing date: {date_str}")
    return new_dates

import matplotlib.pyplot as plt

def plot_trend(data_dict, x):
    df = pd.DataFrame(list(data_dict.items()), columns=[x, "No. of messages"])
    
    fig = px.line(df, x=x, y="No. of messages")
    fig.update_xaxes(title_text=x)
    fig.update_yaxes(title_text="No. of messages")
    
    return fig


def plot_pie_chart_from_df(data_frame, label_column, value_column, limit_labels=8):
    labels = data_frame[label_column]
    values = data_frame[value_column]

    # Sort labels and values in descending order
    sorted_indices = sorted(range(len(values)), key=lambda k: values[k], reverse=True)
    sorted_labels = [labels[i] for i in sorted_indices]
    sorted_values = [values[i] for i in sorted_indices]

    # Group labels beyond the limit into "Others"
    if len(sorted_labels) > limit_labels:
        other_labels = sorted_labels[limit_labels:]
        other_values = sorted_values[limit_labels:]
        sorted_labels = sorted_labels[:limit_labels] + ["Others"]
        sorted_values = sorted_values[:limit_labels] + [sum(other_values)]

    data = {
        label_column: sorted_labels,
        value_column: sorted_values
    }

    df_sorted = pd.DataFrame(data)

    return px.pie(
        df_sorted,
        values=value_column,
        names=label_column,
    )