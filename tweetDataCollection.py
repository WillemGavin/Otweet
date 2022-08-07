# -*- coding: UTF-8 -*-
# 导入 webdriver
import scweet
import datetime

# 从.env获取数据
# period = int(const.get_period(env_path))
# write_mode = const.get_write_mode(env_path)
# save_dir = const.get_save_dir(env_path)
# from_account = const.get_from_account(env_path)
# # 如果不使用代理
# proxy = const.get_proxy(env_path)

def tweet_data_collection(period, write_mode, save_dir, from_account, proxy):
    if period == None or period <= 0:
        period = 7

    if proxy == "None":
        proxy = None
    # print(proxy)
    headless = False
    # 查找tweet中需要包含的词
    words = ['bitcoin']

    # 获取账户粉丝数
    scweet.getAccountFollowerNum(account=from_account[1:], write_mode=write_mode, headless=headless)

    # 根据周期计算开始时间
    since = datetime.date.today() - datetime.timedelta(days=period)
    since = since.strftime('%Y-%m-%d')

    # 爬取账户tweet
    data = scweet.scrape(since=since, from_account=from_account,
                interval=1, display_type="Latest", save_images=False, save_dir=save_dir, headless=headless,
                filter_replies=True, proximity=False, write_mode=write_mode)

    # 爬取@的账户粉丝数及推文信息
    tweet_mention_list = data['mentions']
    for tweet_mention in tweet_mention_list:
        for mention in tweet_mention:
            mention_account = mention[1:]
            print("account:" + mention_account)
            scweet.getAccountFollowerNum(account=mention_account, write_mode=write_mode, headless=headless)
            scweet.scrape(since=since, words=words, from_account=mention,
                interval=1, display_type="Latest", save_images=False, save_dir=save_dir,
                filter_replies=True, proximity=False, write_mode=write_mode)

    return True
    


