import re
def remove_hashtag_mention(tweet):
    try:
        clean_tweet = re.sub("@[A-Za-z0-9_]+", "", tweet)
        clean_tweet = re.sub("#[A-Za-z0-9_]+", "", clean_tweet)
    except:
        return ""
    return clean_tweet

def get_hashtag(tweet):
    hashtags = re.findall("#([a-zA-Z0-9_]{1,50})", tweet)
    return hashtags

def remove_urls(tweet):
    processed_text = re.sub(r"(?:\@|http?\://|https?\://|www)\S+", "", tweet)
    return processed_text