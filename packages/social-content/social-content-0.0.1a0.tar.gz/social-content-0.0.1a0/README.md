## Social Content Parser
A toolkit to parse and analyze contents from social media. 

### Intro

Example 1: Parse Weibo text
```python
from social_content import *
# remove topic tags, links and emoji
text="#1000公里续航新能源车能出吗#  中科院院士欧阳明高表示，如果有人告诉你，这个车能跑1000公里，几分钟能充满电，还很安全，成本又很低。以目前的技术来讲，他一定是骗子！中科院院士的这番言论似乎有所指。蔚来ET7前脚宣布1000公里续航，广汽埃安这几天就向外界公布了全新动力电池科技海报。这几天， ​  展开c"
content=get_plain_text(text)
print(content)
```

Example 2: Evaluate Weibo comment text with emoji
```python
from social_content.weibo import *
'''
    Evaluate sentiment scores based on Weibo user's emoji list
'''
# 1. Chinese comment text
comment="那不也是新能源？如果真想要新能源指标，至于摇号那么久么[中国赞]"
# clean text
comment_cleaned=clean_weibo_text(comment)

# 2. load a list of all possible emojis
happy_emoji,neutral_emoji,sad_emoji=create_emoji_list()

# 3. extract an emoji list in the comment text
list_comment_emoji=extract_emoji(comment)
print("Emoji list:",list_comment_emoji)

# 4. evaluate emoji sentiment based on emoji dictionary and
happy,sad,neutral=sentiment_emoji(happy_emoji,neutral_emoji,sad_emoji,list_comment_emoji)
print(f"Sentiment preference:{happy}\t{sad}\t{neutral}")

# 5. evaluate a combined sentiment, two types of sentiment
avg_sentiment_real,avg_sentiment_grade = get_avg_sentiment_with_all(text=comment_cleaned,list_emoji=list_comment_emoji)
print("Average sentiment by continual value:",avg_sentiment_real)
print("Average sentiment by discrete value: ",avg_sentiment_grade)
```

Example 3: Clean twitter text
```python
from social_content.twitter import *
text='''
#CatBoy called #SafeCatGirl !
https://t.co/CZgF6SJ2RQ
https://t.co/pay2uVyvxL
https://t.co/WeUom7jtEr
#BSCGems #BSCGem #NFT #NFTs #GameFi #ElonMusk #altcoins #bitcoin  
#crypto #ethereum #btc #altcoin #Binance #ripple 
#ETH #shiba #MXS #BNB #dogecoin #Metaverse #BSC #DeFi https://t.co/CHhdHVBuDe https://t.co/fMhOYH1rlO
'''
text=remove_hashtag_mention(text)
text=remove_urls(text)
print(text.strip())
```

### License

The `social-content` toolkit is provided by [Donghua Chen](https://github.com/dhchenx) with MIT License.
