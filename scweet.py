import csv
import imp
import os
import datetime
import time
import random
import pandas as pd
import json
import bs4
import utils
import selenium.webdriver.common.by as cb
import selenium.webdriver.common.action_chains as ac


# 获取用户粉丝数
def getAccountFollowerNum(account, headless=True, write_mode='w', proxy=None, option=None, firefox=False, save_dir="outputs"):
    header = ['ScrapeDate', 'followers', 'followering']

    url = 'https://twitter.com/' + account
    # write mode 
    write_mode = write_mode
    # get date
    date = datetime.date.today().strftime("%Y-%m-%d")
    
    if type(account) == str : 
        account = account.split("//")
        path = save_dir + "/" + '_'.join(account) + '_follow_count.csv'

    # create the <save_dir>
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

            
    time.sleep(random.uniform(1, 2))
    print("访问" + url)

    try:
        driver = utils.init_driver(headless=headless, proxy=proxy, option=option, firefox=firefox)
        driver.get(url)
        time.sleep(random.uniform(3, 5))

        # to_hover = driver.find_element(cb.By.XPATH, value='//div[@data-testid="UserName"]/../div[4]/div[1]/a')
        # ac.ActionChains(driver).move_to_element(to_hover).perform()
        # # time.sleep(random.uniform(1, 2))
        # followers = driver.find_element(cb.By.XPATH, value='//span[@data-testid="HoverLabel"]/span')
        # print(followers.text)
        page_obj = bs4.BeautifulSoup(driver.page_source, 'html.parser')
        scripts = page_obj.find_all('script', type="application/ld+json")
        for script in scripts:
            # print(script.string)
            # user_data = script.text[scripts.find('{') : scripts.rfind('}') + 1]
            # print(user_data)
            data_json = json.loads(script.string)
            if "author" in data_json:
                followers_num = data_json["author"]["interactionStatistic"][0]["userInteractionCount"]
                # print(followers_num)
                followering_num = data_json["author"]["interactionStatistic"][1]["userInteractionCount"]
                # print(followering_num)
                break
    except Exception as e:
        print("出现错误，请稍后重试！或检查用户地址是否正确")
        # ot.update_information("出现错误，请稍后重试！或检查用户地址是否正确")
        error_msg = {'date' : datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S.000Z'), 
        'msg':e, 'url':url}
        error_path = save_dir + "/" + '_error_log.txt'
        with open(error_path, 'a+', newline='', encoding='utf-8') as f:
            f.write(str(error_msg))
        f.close
        return 

    with open(path, write_mode, newline='', encoding='utf-8') as f:
        file = open(path)
        line = len(file.readlines())
        file.close()
        writer = csv.writer(f)
        if write_mode == 'w' or line < 2:
            # write the csv header
            writer.writerow(header)
        else: 
            today_date = datetime.date.today().strftime('%Y-%m-%d')
            last_scrape_date = str(utils.get_last_date_from_csv(path))[:10]
            if last_scrape_date == today_date:
                print(today_date + " scraped, skip this time --------")
                return

        print("followers: ", followers_num)
        data = (date, followers_num, followering_num)
        writer.writerow(data)
        print(url + ': followers and followering Scraped!!!')
    
    return data

# 爬取推文
def scrape(since, until=None, words=None, to_account=None, from_account="ONTOWallet", mention_account=None, interval=5, lang=None,
          headless=True, limit=float("inf"), display_type="Top", proxy=None, hashtag=None, 
          show_images=False, save_images=False, save_dir="outputs", filter_replies=False, proximity=False, 
          geocode=None, minreplies=None, minlikes=None, minretweets=None, write_mode="a+"):
    """
    scrape data from twitter using requests, starting from <since> until <until>. The program make a search between each <since> and <until_local>
    until it reaches the <until> date if it's given, else it stops at the actual date.

    return:
    data : df containing all tweets scraped with the associated features.
    save a csv file containing all tweets scraped with the associated features.
    """

    # ------------------------- Variables : 
    # header of csv
    header = ['ScrapeDate', 'UserScreenName', 'UserName', 'TweetTimestamp', 'Text', 'Embedded_text', 'Emojis', 'Comments', 'Likes', 'Retweets',
                'mentions', 'Image link', 'Tweet URL']
    # list that contains all data 
    data = []
    # unique tweet ids
    tweet_ids = set()
    # write mode 
    write_mode = write_mode

    
    # start scraping from <since> until <until>
    # add the <interval> to <since> to get <until_local> for the first refresh
    until_local = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
    # if <until>=None, set it to the actual date
    if until is None:
        until = datetime.date.today().strftime("%Y-%m-%d")
    # set refresh at 0. we refresh the page for each <interval> of time.
    refresh = 0

    # ------------------------- settings :
    # file path
    # if words:
    #     if type(words) == str : 
    #         words = words.split("//")
    #     path = save_dir + "/" + '_'.join(words) + '_' + str(since).split(' ')[0] + '_' + \
    #            str(until).split(' ')[0] + '.csv'
    # elif from_account:
        # path = save_dir + "/" + from_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
        #     0] + '.csv'
    # elif to_account:
    #     path = save_dir + "/" + to_account + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
    #         0] + '.csv'
    # elif mention_account:
    #     path = save_dir + "/" + mention_account + '_' + str(init_date).split(' ')[0] + '_' + str(max_date).split(' ')[
    #         0] + '.csv'
    # elif hashtag:
    #     path = save_dir + "/" + hashtag + '_' + str(since).split(' ')[0] + '_' + str(until).split(' ')[
    #         0] + '.csv'
    # create the <save_dir>

    path = save_dir + "/" + from_account + '_tweet_statistics' + '.csv'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # show images during scraping (for saving purpose)
    if save_images == True:
        show_images = True
    # initiate the driver
    driver = utils.init_driver(headless, proxy, show_images)
    # resume scraping from previous work
    # if resume:
    today_date = datetime.date.today().strftime('%Y-%m-%d')

    #------------------------- start scraping : keep searching until until
    # open the file
    with open(path, write_mode, newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        file = open(path)
        line = len(file.readlines())
        file.close()
        if write_mode == 'w' or line < 2:
            # write the csv header
            writer.writerow(header)
        else:
            last_scrape_date = str(utils.get_last_date_from_csv(path))[:10]
            if last_scrape_date == today_date:
                print(today_date + " scraped, skip this time --------")
                return None
        # log search page for a specific <interval> of time and keep scrolling unltil scrolling stops or reach the <until>
        while until_local <= datetime.datetime.strptime(until, '%Y-%m-%d'):
            # number of scrolls
            scroll = 0
            # convert <since> and <until_local> to str
            if type(since) != str :
                since = datetime.datetime.strftime(since, '%Y-%m-%d')
            if type(until_local) != str :
                until_local = datetime.datetime.strftime(until_local, '%Y-%m-%d')
            # log search page between <since> and <until_local>
            path = utils.log_search_page(driver=driver, words=words, since=since,
                            until_local=until_local, to_account=to_account,
                            from_account=from_account, mention_account=mention_account, hashtag=hashtag, lang=lang, 
                            display_type=display_type, filter_replies=filter_replies, proximity=proximity,
                            geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
            # number of logged pages (refresh each <interval>)
            refresh += 1
            # number of days crossed
            #days_passed = refresh * interval
            # last position of the page : the purpose for this is to know if we reached the end of the page or not so
            # that we refresh for another <since> and <until_local>
            last_position = driver.execute_script("return window.pageYOffset;")
            # should we keep scrolling ?
            scrolling = True
            print("looking for tweets between " + str(since) + " and " + str(until_local) + " ...")
            print(" path : {}".format(path))
            # number of tweets parsed
            tweet_parsed = 0
            # sleep 
            time.sleep(random.uniform(0.5, 1.5))

            # start scrolling and get tweets
            driver, data, writer, tweet_ids, scrolling, tweet_parsed, scroll, last_position = \
                utils.keep_scroling(driver, data, writer, tweet_ids, scrolling, tweet_parsed, limit, scroll, last_position)

            # keep updating <start date> and <end date> for every search
            if type(since) == str:
                since = datetime.datetime.strptime(since, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                since = since + datetime.timedelta(days=interval)
            if type(since) != str:
                until_local = datetime.datetime.strptime(until_local, '%Y-%m-%d') + datetime.timedelta(days=interval)
            else:
                until_local = until_local + datetime.timedelta(days=interval)

        if data == None or len(data) == 0:
            scrape_date = datetime.date.today().strftime("%Y-%m-%d")
            mockTweet = (scrape_date, '----', '----', '----', '----', '----', '----', 
            '----', '----', '----', '----', '----', '----', )
            writer.writerow(mockTweet)

    data = pd.DataFrame(data, columns = ['ScrapeDate', 'UserScreenName', 'UserName', 'Timestamp', 'Text', 'Embedded_text', 'Emojis', 
                              'Comments', 'Likes', 'Retweets', 'mentions', 'Image link', 'Tweet URL'])

    # save images
    if save_images==True:
        print("Saving images ...")
        save_images_dir = "images"
        if not os.path.exists(save_images_dir):
            os.makedirs(save_images_dir)

        utils.dowload_images(data["Image link"], save_images_dir)

    # close the web driver
    driver.close()

    return data



# if __name__ == '__main__':
#     parser = argparse.ArgumentParser(description='Scrape tweets.')

#     parser.add_argument('--words', type=str,
#                         help='Queries. they should be devided by "//" : Cat//Dog.', default=None)
#     parser.add_argument('--from_account', type=str,
#                         help='Tweets from this account (example : @Tesla).', default=None)
#     parser.add_argument('--to_account', type=str,
#                         help='Tweets replyed to this account (example : @Tesla).', default=None)
#     parser.add_argument('--mention_account', type=str,
#                         help='Tweets mention a account (example : @Tesla).', default=None)
#     parser.add_argument('--hashtag', type=str, 
#                         help='Hashtag', default=None) 
#     parser.add_argument('--until', type=str,
#                         help='Max date for search query. example : %%Y-%%m-%%d.', required=True)
#     parser.add_argument('--since', type=str,
#                         help='Start date for search query. example : %%Y-%%m-%%d.', required=True)
#     parser.add_argument('--interval', type=int,
#                         help='Interval days between each start date and end date for search queries. example : 5.',
#                         default=1)
#     parser.add_argument('--lang', type=str,
#                         help='Tweets language. example : "en" for english and "fr" for french.', default=None)
#     parser.add_argument('--headless', type=bool,
#                         help='Headless webdrives or not. True or False', default=False)
#     parser.add_argument('--limit', type=int,
#                         help='Limit tweets per <interval>', default=float("inf"))
#     parser.add_argument('--display_type', type=str,
#                         help='Display type of twitter page : Latest or Top', default="Top")
#     parser.add_argument('--resume', type=bool,
#                         help='Resume the last scraping. specify the csv file path.', default=False)
#     parser.add_argument('--proxy', type=str,
#                         help='Proxy server', default=None)
#     parser.add_argument('--proximity', type=bool,
#                         help='Proximity', default=False)                        
#     parser.add_argument('--geocode', type=str,
#                         help='Geographical location coordinates to center the search, radius. No compatible with proximity', default=None)
#     parser.add_argument('--minreplies', type=int,
#                         help='Min. number of replies to the tweet', default=None)
#     parser.add_argument('--minlikes', type=int,
#                         help='Min. number of likes to the tweet', default=None)
#     parser.add_argument('--minretweets', type=int,
#                         help='Min. number of retweets to the tweet', default=None)
                            

#     args = parser.parse_args()

#     words = args.words
#     until = args.until
#     since = args.since
#     interval = args.interval
#     lang = args.lang
#     headless = args.headless
#     limit = args.limit
#     display_type = args.display_type
#     from_account = args.from_account
#     to_account = args.to_account
#     mention_account = args.mention_account
#     hashtag = args.hashtag
#     resume = args.resume
#     proxy = args.proxy
#     proximity = args.proximity
#     geocode = args.geocode
#     minreplies = args.minreplies
#     minlikes = args.minlikes
#     minretweets = args.minlikes

#     data = scrape(since=since, until=until, words=words, to_account=to_account, from_account=from_account, mention_account=mention_account,
#                 hashtag=hashtag, interval=interval, lang=lang, headless=headless, limit=limit,
#                 display_type=display_type, resume=resume, proxy=proxy, filter_replies=False, proximity=proximity,
#                 geocode=geocode, minreplies=minreplies, minlikes=minlikes, minretweets=minretweets)
