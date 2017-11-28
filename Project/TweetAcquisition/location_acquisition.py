
import sys
from bs4 import BeautifulSoup
import pickle
import pandas as pd
import os
import requests
import time
import datetime
import random

def main(argv):

    if len(argv) > 1 :
        path_name = str(argv[1])
        if not(os.path.isdir(s=path_name)):
            print('Input folder was incorrect, please try again with another path.')
            return
    else:
        print('Input folder was incorrect, please try again with another path.')
        return

    case_name = path_name.split(sep='/')[-1] # CORRECT THIS
    #log_save = path_name + case_name + '_' + 'located.log'
    prefix_name = 'Located'
    file_name = 'Tweets'


    while True:

        tweets_files = get_pickle_name(path_name,prefix_name, file_name)
        if tweets_files == []:
            print('No tweet pickle available, trying again in 2 min ...')
            time.sleep(2*60)
        else:
            tweets_file_name = tweets_files[0]
            # creating the empty final pickle in order to run multiple codes
            file_save = '{}{}_{}'.format(path_name, prefix_name,tweets_file_name)
            open(file_save,'a').close()
            print('Let us retrieve location for : {}'.format(tweets_file_name))

            ### Retrieving the locations for every tweet of every pickle.
            # Load the tweets dataframe from the pickle
            tweet_df = pickle.load(open(path_name + tweets_file_name, 'rb'))
            loc_dict = get_locations(tweet_df)
            tweet_df['location'] = pd.Series(loc_dict)

            #print(tweet_df)
            # Saving the new location pickle
            with open(file_save, 'wb') as handle:
                pickle.dump(tweet_df, handle, protocol=pickle.HIGHEST_PROTOCOL)


def get_pickle_name(path_name,prefix_name,file_name):
    # Retrieving the list of elements in the folder.
    files_list = os.listdir(path_name)
    # Loking at which elelement location are missing : (missing prefic : 'Located_' )
    located_tweets = []
    original_tweets = []
    for f in files_list:
        first_part_str = f.split(sep='_')[0]
        if first_part_str == prefix_name:
            located_tweets.append(f)
        elif first_part_str == file_name:
            original_tweets.append(f)
    total = len(original_tweets)
    # Establishing the list of not treated elelements.
    for f in located_tweets:
        s = '_'.join(f.split('_')[1:])
        try:
            original_tweets.remove(s)
        except:
            print(s)
            print(original_tweets)

    print('There are {} on {} pickles left to handle'.format(len(original_tweets),total))
    print('---------------------------------------------------------------------------')
    return original_tweets

def get_locations(tweet_df):
    base_url = 'https://twitter.com/'

    locations = {}
    t = time.time()
    max_i = len(tweet_df) # FOR TESTING : .head(5)
    ev = 0
    print('% ',end='', flush=True)
    for i in range(max_i): # TOCHANGE
        user_name = tweet_df['user_name'][i]
        url = base_url + user_name
        try:
            r = requests.get(url=url)
            soup = BeautifulSoup(r.text,'lxml')
            loc = (soup.find('span',class_='ProfileHeaderCard-locationText').text.replace('\n','').split(' '))
            locations[i] = [e for e in loc if e != '']
        except:
            locations[i] = []
            print('*',end='', flush=True)

        if int(100*i/max_i)> ev:
            ev += 1
            print('|',end='', flush=True)
        time.sleep(random.uniform(0,1))
    elapsed_time = time.time() - t

    print(' % ')
    print('Elapsed Time : {:.2f} s - Rate : {:.2f} tw/s - Finished at : {}'.format(elapsed_time , max_i/elapsed_time,datetime.datetime.now()), flush=True)
    print('---------------------------------------------------------------------------')
    return locations



if __name__ == "__main__":
    main(sys.argv)
