def preprocess(data):
    import re
    import  pandas as pd


    messages_raw = re.split(r"(?=\d{2}/\d{2}/\d{4}, \d{1,2}:\d{2}\s?\u202f?[ap]m - )", data)

    user_pattern = r"(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\s?\u202f?[ap]m) - ([^:]+): (.+)"
    system_pattern = r"(\d{2}/\d{2}/\d{4}), (\d{1,2}:\d{2}\s?\u202f?[ap]m) - (.+)"

    dates = []
    messages = []

    for msg in messages_raw:
        msg = msg.strip()
        if not msg:
            continue

        user_match = re.match(user_pattern, msg)
        system_match = re.match(system_pattern, msg)

        if user_match:
            date_str = user_match.group(1)
            time_str = user_match.group(2).replace('\u202f', ' ')
            full_datetime = f"{date_str} {time_str}"
            sender = user_match.group(3)
            message = user_match.group(4)
            formatted_message = f"{sender}: {message}"
        elif system_match:
            date_str = system_match.group(1)
            time_str = system_match.group(2).replace('\u202f', ' ')
            full_datetime = f"{date_str} {time_str}"
            message = system_match.group(3)
            formatted_message = f"System: {message}"
        else:
            continue

        dates.append(full_datetime)
        messages.append(formatted_message)

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})

    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y %I:%M %p")

    df.rename(columns={'message_date': 'date'}, inplace=True)

    df[['user', 'message']] = df['user_message'].str.split(': ', n=1, expand=True)
    df['date'] = pd.to_datetime(df['date'])
    df.drop(columns=['user_message'], inplace=True)
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['weekday'] = df['date'].dt.day_name()
    df['only_date'] = df['date'].dt.day
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    return df