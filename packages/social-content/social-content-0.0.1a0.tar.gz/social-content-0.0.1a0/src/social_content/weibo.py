import time
import re
import jieba
from nerkit.StanzaApi import StanzaWrapper

def convert_to_standard_time(s):
    s=s.replace("+0800","")
    return time.strftime("%Y-%m-%d %H:%M:%S", time.strptime(s, "%a %b %d %H:%M:%S %Y"))

def remove_weibo_tags(str):
    str = re.sub(
        re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', re.DOTALL), '',
        str)
    pattern = re.compile(r'#[^#]*#', re.S)
    result = pattern.sub('', str)
    return result

def extract_emoji(str):
    result=re.findall(r"\[([\w+]+)\]", str)
    list_r=[]
    for r in result:
        if r not in list_r:
            list_r.append(f"[{r}]")
    return list_r

def remove_emoji(str):
    pattern = re.compile(r"\[[\w+]+\]", re.S)
    result = pattern.sub('', str)
    return result

def get_plain_text(s):
    return remove_emoji(remove_weibo_tags(s)).strip()

def simple_word_segmentation(str):
    seg_list = jieba.cut(str, cut_all=False)
    r_list=[]
    for w in seg_list:
        if w.strip()=="":
            continue
        r_list.append(w.strip())
    return r_list

def clean_text(rgx_list, text):
    new_text = text
    for rgx_match in rgx_list:
        new_text = re.sub(rgx_match, '', new_text)
    return new_text

def clean_weibo_text(text):
    text = clean_text(['#(.*)#', '【(.*)】',"@(\w*)\s*"], text)

    text = text.replace("【", "")
    text = text.replace("】", "")
    text = text.replace("展开c", "")
    text = text.replace("​", "")
    text=text.replace("？","")
    text=text.replace(" ","")
    text = text.strip()
    return text

def create_emoji_list(happy_emoji=None,sad_emoji=None,neutral_emoji=None):
    if happy_emoji==None:
        happy_emoji=['good','中国赞','打call','鼓掌','赞','笑而不语','笑cry','哈哈','加油','给力','鲜花','太开心','微笑','心','太阳','笑哈哈','偷乐','嘻嘻','喵喵','给你小心心','耶','音乐','赞啊',
                 '偷笑','可爱','送花花','哇','爱你' ,'愛你','好爱哦','锦鲤','好喜欢','微笑趣泡','喜','机智','棒棒糖','牛哞哞','烟花','贊','鮮花','亲亲','掌宝爱心','星星','礼物','給力','哆啦A梦微笑',
                 '带感','太陽','ali笑','贊啊','太開心','奥克耶','666','贏牛奶','酷','顶'
                 ]
    if sad_emoji==None:
        sad_emoji=[
        '允悲','费解','求饶','泪','苦涩','悲伤','伤心','抓狂','失望','抱抱','蠟燭','怒','哼','怒骂','生病','鄙视','疑问','可怜','裂开','傻眼','酸','跪了','衰','困','哆啦A夢害怕','打脸',
        '捂脸','吃惊','淚','委屈','怒罵','哈欠','打臉','白眼','弱','睡','阴险'
               ]
    if neutral_emoji==None:
        neutral_emoji=[
        '思考','并不简单','围观','ok','举手'
        ]
    return happy_emoji,neutral_emoji,sad_emoji

def sentiment_emoji( happy_emoji,neutral_emoji,sad_emoji,list_emoji):
    list_all_emoji=happy_emoji+sad_emoji+neutral_emoji
    if len(list_emoji)==0:
        return 0,0,0
    N=0
    happy=0
    sad=0
    neutral=0
    for emoji in list_emoji:
        e=emoji.replace("[","").replace("]","")
        if e in happy_emoji:
            happy+=1
        if e in sad_emoji:
            sad+=1
        if e in neutral_emoji:
            neutral+=1
        if e in list_all_emoji:
            N+=1
    if N==0:
        return 0,0,0
    return round(happy/N,4),round(sad/N,4),round(neutral/N,4)

def get_mean_emoji_sentiment(s_happy,s_sad,s_neutral):
    if s_happy>s_sad and s_happy>s_neutral:
        return 2
    if s_sad>s_happy and s_sad>s_neutral:
        return 0
    return 1

def get_mean_emoji_sentiment_revised(s_happy,s_sad,s_neutral):
    if s_happy>s_sad and s_happy>s_neutral:
        return 1+s_happy
    if s_sad>s_happy and s_sad>s_neutral:
        return 1-s_sad
    return 1

def get_avg_sentiment_revised(s_text,s_happy,s_sad,s_neutral):
    r_text=s_text*1.0/2
    r_emoji=get_mean_emoji_sentiment_revised(s_happy,s_sad,s_neutral)*1.0/2
    return (r_text+r_emoji)*1.0/2

def get_avg_sentiment(s_text,s_happy,s_sad,s_neutral):
    r_text=s_text*1.0/2
    r_emoji=get_mean_emoji_sentiment(s_happy,s_sad,s_neutral)*1.0/2
    return (r_text+r_emoji)*1.0/2

def get_avg_sentiment_with_all(sw=None,text="",list_emoji=[],happy_emoji=[],neutral_emoji=[],sad_emoji=[]):
    if sw==None:
        sw = StanzaWrapper()
    s_happy, s_sad, s_neutral = sentiment_emoji(happy_emoji=happy_emoji,neutral_emoji=neutral_emoji,sad_emoji=sad_emoji,list_emoji=list_emoji)
    text_sentiment = sw.sentiment_chinese(text)
    s_text_sum = 0
    s_text = 0.5
    if len(text_sentiment) != 0:
        for l in text_sentiment:
            v = l["sentiment"]
            s_text_sum += int(v)
        s_text = s_text_sum * 1.0 / len(text_sentiment)
    avg_sentiment_grade = get_avg_sentiment(s_text, s_happy, s_sad, s_neutral)
    avg_sentiment_real = get_avg_sentiment_revised(s_text, s_happy, s_sad, s_neutral)
    return avg_sentiment_real,avg_sentiment_grade