import re
import pandas as pd


def iosdata(data):
    all_data = []
    if data.startswith('['):
        pattern = r"\[\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}:\d{2}\s[A|P]M]\s"
        content = re.split(pattern, data)[1:]

    for x in content:
        all_data.append(x.strip())
    date = []
    dates = re.findall(pattern, data)

    for dat in dates:
        date.append(dat.strip().replace('[', '').replace(']', ''))

    df = pd.DataFrame({'date': date, 'message': all_data})

    users = []
    messages = []

    for message in df['message']:
        x = message.split(':')
        if len(x) > 1:
            users.append(x[0])
            messages.append(x[1])
        else:
            users.append('group notification')
            messages.append(x[0])

    df['user'] = users
    df['messages'] = messages

    df.drop('message', axis=1, inplace=True)

    df['date'] = pd.to_datetime(df['date'],format = '%d/%m/%y, %I:%M:%S %p')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['weekname'] = df['date'].dt.day_name()

    return df


def androiddata(data):
    pattern = r"\d{1,2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s[a|p]m"
    dates = re.findall(pattern, data)
    date = list(dates)
    content = re.split(pattern, data)[1:]

    message = []
    for msg in content:
        message.append(msg.strip().replace('-', ''))
    df = pd.DataFrame({'date': date, 'message': message})

    users = []
    message = []
    for msg in df['message']:
        x = msg.split(':')
        if len(x) > 1:
            users.append(x[0])
            message.append(x[1])
        else:
            users.append('group notification')
            message.append(x[0])

    df['user'] = users
    df['messages'] = message
    df.drop('message', axis=1, inplace=True)
    df['date'] = pd.to_datetime(df['date'],format = '%d/%m/%Y, %I:%M %p')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute
    df['weekname'] = df['date'].dt.day_name()

    return df


