from textblob import TextBlob

def analyze_sentiment(text, hashtags=None):
    polarity = TextBlob(text).sentiment.polarity

    if hashtags:
        for hashtag in hashtags:
            hashtag_sentiment = TextBlob(hashtag).sentiment.polarity
            if hashtag_sentiment > 0:
                polarity += 0.1
            elif hashtag_sentiment < 0:
                polarity -= 0.1

    if polarity >= 0.5:
        return 'Very Positive'
    elif 0.1 <= polarity < 0.5:
        return 'Positive'
    elif -0.1 < polarity < 0.1:
        return 'Neutral'
    elif -0.5 <= polarity <= -0.1:
        return 'Negative'
    else:
        return 'Very Negative'


def convert_to_int(value_str):
    """
    Converts string like '1.5k' or '3.2m' to integer (e.g., '1.5k' → 1500)
    """
    try:
        value_str = value_str.strip().lower().replace(',', '')
        if 'k' in value_str:
            return int(float(value_str.replace('k', '')) * 1000)
        elif 'm' in value_str:
            return int(float(value_str.replace('m', '')) * 1000000)
        else:
            return int(float(value_str))
    except:
        return 0

def calculate_engagement(followers, likes, comments):
    try:
        followers = convert_to_int(followers)
        likes = int(likes)
        comments = int(comments)

        if followers <= 0:
            return 0.0

        engagement = ((likes + comments) / followers) * 100
        return round(min(engagement, 100.0), 2)
    except:
        return 0.0
