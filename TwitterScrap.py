import tweepy
import telegram
from datetime import datetime
from time import sleep

# if __name__ == '__main__':
# 트위터 설정
api_key = "*"
api_secret = "*"  
access_token = "*"
access_secret = "*"
auth = tweepy.OAuthHandler(api_key, api_secret)
auth.set_access_token(access_token, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)

# 텔레그램 설정
bot = telegram.Bot(token="*")
chat_id = "*"

# 처음 실행시 트윗들을 리스트에 저장 및 텔레그램 봇 발신
latestTwits = list()
try :
    twits = api.home_timeline()
    for twit in twits:
        if twit not in latestTwits:
            latestTwits.append(twit)
    latestTwits.reverse() # 트윗 날짜 내림차순 -> 오름차순
    i = 0
    while i < len(latestTwits):
        messageQueue = "[" + latestTwits[i].user.name + "@" + latestTwits[i].user.screen_name + "]" + "\n" + latestTwits[i].text
        print(messageQueue)
        bot.sendMessage(chat_id=chat_id, text=messageQueue)
        i = i + 1
    sleep(5 * 60) # 5분 대기
except tweepy.RateLimitError: # 트위터 API 자주 호출하면 RateLimitError 발생
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] 트위터 API RateLimitError 발생! 15분 대기합니다")
    sleep(15 * 60) # 15분 대기
except:
    print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Error 발생! 15분 대기합니다")
    sleep(15 * 60) # 15분 대기

# 이후 무한 반복
while True:
    try:
        tempTwits = list()
        twits = api.home_timeline()
        for twit in twits:
            if twit not in latestTwits:
                tempTwits.append(twit)
        tempTwits.reverse()
        i = 0
        while i < len(tempTwits): # 다시 받아온 트윗 리스트(tempTwits)를 마지막 트윗 리스트(latestTwits)와 비교한다
            if tempTwits[i] in latestTwits: # 이미 있는 트윗이면 넘긴다
                i = i + 1
            else: # 새로운 트윗이면 기존 리스트에서 가장 오래된 트윗을 하나 비우고 새로 추가한다
                if len(latestTwits) > 20: # api.home_timeline() 함수가 최대 20개밖에 못가져오므로 제일 오래된거 하나 비움
                    del latestTwits[0]
                latestTwits.append(tempTwits[i])
                messageQueue = "[" + tempTwits[i].user.name + "@" + tempTwits[i].user.screen_name + "]" + "\n" + tempTwits[i].text
                print(messageQueue)
                bot.sendMessage(chat_id=chat_id, text=messageQueue)
                i = i + 1
        sleep(5 * 60) # 5분 대기
    except tweepy.RateLimitError: # 트위터 API 자주 호출하면 RateLimitError 발생
        print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] 트위터 API RateLimitError 발생! 15분 대기합니다")
        sleep(15 * 60) # 15분 대기
    except:
        print("[" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "] Error 발생! 15분 대기합니다")
        sleep(15 * 60) # 15분 대기
