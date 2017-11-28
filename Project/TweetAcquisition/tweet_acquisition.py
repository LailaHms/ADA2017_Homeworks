import urllib.parse
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
import datetime
from TweetCriteria import TweetCriteria
import random
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import re



def main(argv):

    max_scroll = 500  # Maximal number of tweets inside a query
    path_save = './Nigeria_1/'
    log_save = path_save + 'Nigeria_1.log'
    file_save = 'Tweets'
    log_file = open(log_save,'a')

    print('------------------------------------------- ACQUISITION PARAMETERS -------------------------------------------')
    print('------------------------------------------- ACQUISITION PARAMETERS -------------------------------------------',file=log_file)
    print('Started at : {}'.format(str(datetime.datetime.now())))
    print('Started at : {}'.format(str(datetime.datetime.now())),file=log_file)

    print('Tweets saved in {}'.format(path_save))
    print('Tweets saved in {}'.format(path_save),file=log_file)

    # Paris Shooting January 2015 :
    hashtags = ['Dalori','Dalorilivesmatter','BokoHaram','Bokoharam','bokoharam','Borno','StopBokoHaram','PrayForNigeria']


    date_start = '2016-01-29'  # one day before the event
    date_stop = '2016-02-06'  # one week after the event

    print('Searching from {} to {}'.format(date_start, date_stop))
    print('Searching from {} to {}'.format(date_start, date_stop),file=log_file)
    print( 'Hastags used : {}'.format(hashtags))
    print('Hastags used : {}'.format(hashtags),file=log_file)




    state = 0
    last_id = 0
    n_acqu_total = 0
    k = 0
    total_time = 0

    # Load the pickle to resume the acquisition

    if len(argv) > 1:
        try:
            load_name = str(argv[1])
            tweet_df = pickle.load(open(load_name, 'rb'))
            numbers_in_name = re.findall('\d+', load_name)
            k = int(numbers_in_name[-1])
            state = 1
            last_id = str(int(tweet_df['id'].tolist()[-1]) - 1)

            print(' Resuming the acquisition from tweet : {}'.format(last_id))
            print(' Resuming the acquisition from tweet : {}'.format(last_id),file=log_file)

        except:
            print('Input file was incorrect, please try again with another file or path.')
            return

    print('------------------------------------------- STARTING ACQUISITION -------------------------------------------')
    print('------------------------------------------- STARTING ACQUISITION -------------------------------------------',file=log_file)

    log_file.close()

    # Opening the browser with selenium and PhantomJS/Chrome
    navigator = open_navigator()


    while state != 2:

        t = time.time()  # timing
        if state == 0:
            criteria = TweetCriteria().setSince(date_start).setUntil(date_stop)
        elif state == 1:
            criteria = TweetCriteria().setSince(date_start).setMaxId(last_id)

        url = url_search_generator(hashtags, criteria)

        navigator.get(url)

        # Now scroll down the page for a while

        scroll_down(navigator,max_scroll)

        # Now get the HTML with beautiful Soup

        tweets = get_tweet_info(navigator)

        k += 1


        n_acqu = len(tweets['id'])
        n_acqu_total += n_acqu  # incrementing the total counter

        tweet_df = pd.DataFrame(tweets)
        tweet_df['date'] = pd.to_datetime(tweet_df['time_stamp'], unit='s') # transforming the timestamp into datetime format

        last_id = tweet_df['id'].tolist()[-1]
        last_tweet_date = str(tweet_df['date'].tolist()[-1].date())

        elapsed_time = time.time() - t
        total_time += elapsed_time

        print_acquisition(k, n_acqu, n_acqu_total, str(tweet_df['date'].tolist()[0]), str(tweet_df['date'].tolist()[-1]), total_time, elapsed_time,log_save)

        # Saving Data :
        with open('{}{}_{}.pickle'.format(path_save, file_save, k), 'wb') as handle:
            pickle.dump(tweet_df, handle, protocol=pickle.HIGHEST_PROTOCOL)

        if state == 0:
            state = 1

        if last_tweet_date == date_start:
            state = 2
            log_file = open(log_save,'a')
            print('------------------ ALL TWEETS WERE AQUIRED ------------------')
            print('------------------ ALL TWEETS WERE AQUIRED ------------------',file=log_file)
            log_file.close()
            navigator.close()
            user_navigator.close()


def print_acquisition(k,n_acqu,n_acqu_total,first_tweet_date,last_tweet_date,total_time,elapsed,log_save):
    rate = n_acqu/elapsed
    log_file = open(log_save,'a')
    # Printing outputs :
    output = '{} - Tweets : {} - Total : {} - Date : {} - Elapsed Time : {:.3f} s - Delay : {:.3f} s - Rate : {:.3f} tw/s - Executed at {}'.format(
        k,
        n_acqu,
        n_acqu_total,
        last_tweet_date,
        total_time,
        elapsed,
        rate,
        str(datetime.datetime.now()))
    print(output)
    print(output,file=log_file)
    print('     + First Tweet Time : {}'.format(first_tweet_date))
    print('     + First Tweet Time : {}'.format(first_tweet_date),file=log_file)
    print('     + Last Tweet Time : {}'.format(last_tweet_date))
    print('     + Last Tweet Time : {}'.format(last_tweet_date),file=log_file)
    print(' ')
    print(' ',file=log_file)

    log_file.close()



def open_navigator(choice='phantomJS'):
    if choice == 'phantomJS':

        navigator = webdriver.PhantomJS(desired_capabilities=set_user_agent()) # service_args=['--load-images=[false]']
    else:
        navigator = webdriver.Chrome()
    return navigator


def set_user_agent():

    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36"
        "(KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
    )
    return dcap


def url_user_generator(user):
    url = "https://twitter.com/"

    return url


def url_search_generator(hashtags,tweetCriteria):

    # transforming the hashtag list into a search query
    query = ' '
    for i in range(len(hashtags)):
        if i == len(hashtags) - 1:
            query += '#' + hashtags[i]
        else:
            query += '#' + hashtags[i] + ' OR '

    tweetCriteria.setQuerySearch(query)


    # create URL for the query :
    url = "https://twitter.com/search?q={}&src=typd"
    urlGetData = ''
    if hasattr(tweetCriteria, 'username'):
        urlGetData += ' from:' + tweetCriteria.username

    if hasattr(tweetCriteria, 'querySearch'):
        urlGetData += ' ' + tweetCriteria.querySearch

    if hasattr(tweetCriteria, 'near'):
        urlGetData += "&near:" + tweetCriteria.near + " within:" + tweetCriteria.within

    if hasattr(tweetCriteria, 'since'):
        urlGetData += ' since:' + tweetCriteria.since

    if hasattr(tweetCriteria, 'until'):
        urlGetData += ' until:' + tweetCriteria.until

    if hasattr(tweetCriteria, 'maxId'):
        urlGetData += ' max_id:' + tweetCriteria.maxId

    if hasattr(tweetCriteria, 'sinceId'):
        urlGetData += ' since_id:' + tweetCriteria.sinceId

    if hasattr(tweetCriteria, 'topTweets'):
        if tweetCriteria.topTweets:
            url = "https://twitter.com/i/search/timeline?q=%s&src=typd&max_position=%s"


    # Formating the URL
    url = url.format(urllib.parse.quote(str(urlGetData), encoding='utf-8'))
    print('Query URL : {} '.format(url))
    return url


def scroll_down(navigator, max_scroll):
    k = 0
    while k < max_scroll:
        k +=1
        navigator.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(random.uniform(0.8, 1.2));
        if k % random.choice([5,10,15]) == 0:
            time.sleep(random.uniform(2, 5));
            # ADD SOME RANDOM BEHAVIORS


def get_tweet_info(navigator):
    html = navigator.page_source
    soup = BeautifulSoup(html, 'lxml')

    tweet_text = [p.text for p in soup.findAll('p', class_='tweet-text')]

    lang = [p.attrs['lang'] for p in soup.findAll('p', class_='tweet-text')]
    time_stamp = [int(p.contents[0].attrs['data-time']) for p in soup.findAll('a', class_='tweet-timestamp')]

    tweet_id = [p.attrs['data-tweet-id'] for p in soup.findAll('div', class_='js-stream-tweet')]
    user_id = [p.attrs['data-user-id'] for p in soup.findAll('div', class_='js-stream-tweet')]
    user_name = [p.attrs['data-screen-name'] for p in soup.findAll('div', class_='js-stream-tweet')]
    hashtags = []
    bloc_list = soup.findAll('p', class_='tweet-text')
    for i in range(len(bloc_list)):
        b = bloc_list[i]
        hashtags.append([])
        for j in range(len(b.contents)):
            try:
                hashtags[i].append(b.contents[j].text)
            except:
                pass

    tweet_dict = {'id': tweet_id,'text':tweet_text, 'time_stamp': time_stamp,'language': lang, 'user_name': user_name, 'user_id': user_id,'hashtags': hashtags}
    return tweet_dict


if __name__ == "__main__":
    main(sys.argv)
